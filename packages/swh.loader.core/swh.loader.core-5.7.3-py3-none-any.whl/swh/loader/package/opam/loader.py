# Copyright (C) 2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import io
import os
from subprocess import PIPE, Popen, call
from typing import Any, Iterator, List, Optional, Tuple

import attr

from swh.loader.package.loader import (
    BasePackageInfo,
    PackageLoader,
    RawExtrinsicMetadataCore,
)
from swh.loader.package.utils import cached_method
from swh.model.model import (
    MetadataAuthority,
    MetadataAuthorityType,
    ObjectType,
    Person,
    Release,
    Sha1Git,
)
from swh.storage.interface import StorageInterface


@attr.s
class OpamPackageInfo(BasePackageInfo):
    author = attr.ib(type=Person)
    committer = attr.ib(type=Person)


def opam_read(
    cmd: List[str], init_error_msg_if_any: Optional[str] = None
) -> Optional[str]:
    """This executes an opam command and returns the first line of the output.

    Args:
        cmd: Opam command to execute as a list of string
        init_error_msg_if_any: Error message to raise in case a problem occurs
          during initialization

    Raises:
        ValueError with the init_error_msg_if_any content in case stdout is not
        consumable and the variable is provided with non empty value.

    Returns:
        the first line of the executed command output

    """
    with Popen(cmd, stdout=PIPE) as proc:
        if proc.stdout is not None:
            for line in io.TextIOWrapper(proc.stdout):
                # care only for the first line output result (mostly blank separated
                # values, callers will deal with the parsing of the line)
                return line
        elif init_error_msg_if_any:
            raise ValueError(init_error_msg_if_any)
    return None


class OpamLoader(PackageLoader[OpamPackageInfo]):
    """Load all versions of a given package in a given opam repository.

    The state of the opam repository is stored in a directory called an opam root. This
    folder is a requisite for the opam binary to actually list information on package.

    When initialize_opam_root is False (the default for production workers), the opam
    root must already have been configured outside of the loading process. If not an
    error is raised, thus failing the loading.

    For standalone workers, initialize_opam_root must be set to True, so the ingestion
    can take care of installing the required opam root properly.

    The remaining ingestion uses the opam binary to give the versions of the given
    package. Then, for each version, the loader uses the opam binary to list the tarball
    url to fetch and ingest.

    """

    visit_type = "opam"

    def __init__(
        self,
        storage: StorageInterface,
        url: str,
        opam_root: str,
        opam_instance: str,
        opam_url: str,
        opam_package: str,
        initialize_opam_root: bool = False,
        **kwargs: Any,
    ):
        super().__init__(storage=storage, url=url, **kwargs)

        self.opam_root = opam_root
        self.opam_instance = opam_instance
        self.opam_url = opam_url
        self.opam_package = opam_package
        self.initialize_opam_root = initialize_opam_root

    def get_package_dir(self) -> str:
        return (
            f"{self.opam_root}/repo/{self.opam_instance}/packages/{self.opam_package}"
        )

    def get_package_name(self, version: str) -> str:
        return f"{self.opam_package}.{version}"

    def get_package_file(self, version: str) -> str:
        return f"{self.get_package_dir()}/{self.get_package_name(version)}/opam"

    def get_metadata_authority(self):
        return MetadataAuthority(type=MetadataAuthorityType.FORGE, url=self.opam_url)

    @cached_method
    def _compute_versions(self) -> List[str]:
        """Compute the versions using opam internals

        Raises:
            ValueError in case the lister is not able to determine the list of versions

        Returns:
            The list of versions for the package

        """
        # TODO: use `opam show` instead of this workaround when it support the `--repo`
        # flag
        package_dir = self.get_package_dir()

        if not os.path.exists(package_dir):
            raise ValueError(
                f"can't get versions for package {self.opam_package} "
                f"(at url {self.origin.url})."
            )

        versions = [
            ".".join(version.split(".")[1:]) for version in os.listdir(package_dir)
        ]
        if not versions:
            raise ValueError(
                f"can't get versions for package {self.opam_package} "
                f"(at url {self.origin.url})"
            )
        versions.sort()
        return versions

    def get_versions(self) -> List[str]:
        """First initialize the opam root directory if needed then start listing the
        package versions.

        Raises:
            ValueError in case the lister is not able to determine the list of
            versions or if the opam root directory is invalid.

        """
        if self.initialize_opam_root:
            # for standalone loader (e.g docker), loader must initialize the opam root
            # folder
            call(
                [
                    "opam",
                    "init",
                    "--reinit",
                    "--bare",
                    "--no-setup",
                    "--root",
                    self.opam_root,
                    self.opam_instance,
                    self.opam_url,
                ]
            )
        else:
            # for standard/production loaders, no need to initialize the opam root
            # folder. It must be present though so check for it, if not present, raise
            if not os.path.isfile(os.path.join(self.opam_root, "config")):
                # so if not correctly setup, raise immediately
                raise ValueError("Invalid opam root")

        return self._compute_versions()

    def get_default_version(self) -> str:
        """Return the most recent version of the package as default."""
        return self._compute_versions()[-1]

    def _opam_show_args(self, version: str):
        package_file = self.get_package_file(version)

        return [
            "opam",
            "show",
            "--color",
            "never",
            "--safe",
            "--normalise",
            "--root",
            self.opam_root,
            "--file",
            package_file,
        ]

    def get_enclosed_single_line_field(self, field, version) -> Optional[str]:
        result = opam_read(self._opam_show_args(version) + ["--field", field])

        # Sanitize the result if any (remove trailing \n and enclosing ")
        return result.strip().strip('"') if result else None

    def get_package_info(self, version: str) -> Iterator[Tuple[str, OpamPackageInfo]]:

        url = self.get_enclosed_single_line_field("url.src:", version)
        if url is None:
            raise ValueError(
                f"can't get field url.src: for version {version} of package"
                f" {self.opam_package} (at url {self.origin.url}) from `opam show`"
            )

        checksums_str = self.get_enclosed_single_line_field("url.checksum:", version)
        checksums = {}
        if checksums_str:
            for c in checksums_str.strip("[]").split(" "):
                algo, hash = c.strip('"').split("=")
                checksums[algo] = hash

        authors_field = self.get_enclosed_single_line_field("authors:", version)
        fullname = b"" if authors_field is None else str.encode(authors_field)
        author = Person.from_fullname(fullname)

        maintainer_field = self.get_enclosed_single_line_field("maintainer:", version)
        fullname = b"" if maintainer_field is None else str.encode(maintainer_field)
        committer = Person.from_fullname(fullname)

        with Popen(self._opam_show_args(version) + ["--raw"], stdout=PIPE) as proc:
            assert proc.stdout is not None
            metadata = proc.stdout.read()

        yield self.get_package_name(version), OpamPackageInfo(
            url=url,
            filename=None,
            author=author,
            committer=committer,
            version=version,
            directory_extrinsic_metadata=[
                RawExtrinsicMetadataCore(
                    metadata=metadata,
                    format="opam-package-definition",
                )
            ],
            checksums=checksums,
        )

    def build_release(
        self,
        p_info: OpamPackageInfo,
        uncompressed_path: str,
        directory: Sha1Git,
    ) -> Optional[Release]:

        msg = (
            f"Synthetic release for OPAM source package {self.opam_package} "
            f"version {p_info.version}\n"
        )
        return Release(
            name=p_info.version.encode(),
            author=p_info.author,
            message=msg.encode(),
            date=None,
            target=directory,
            target_type=ObjectType.DIRECTORY,
            synthetic=True,
        )
