
# src\file_conversor\dependency\scoop_pkg_manager.py

import os
import shutil

from pathlib import Path

# user-provided imports
from file_conversor.system import _PLATFORM_WINDOWS

from file_conversor.config import Environment, Log
from file_conversor.config.locale import get_translation

from file_conversor.dependency.abstract_pkg_manager import AbstractPackageManager

_ = get_translation()
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class ScoopPackageManager(AbstractPackageManager):
    def __init__(self,
                 dependencies: dict[str, str],
                 env: list[str | Path] | None = None,
                 buckets: list[str] | None = None,
                 ) -> None:
        """
        Inits Scoop pkg manager.

        :param dependencies: Format {executable: dependency}
        :param env: Environment PATHs to add, to allow dependency finding.
        :param buckets: Buckets to add, to allow dependency install.
        """
        super().__init__(
            dependencies,
            env=env,
        )
        self._buckets = buckets if buckets else []

        self.add_pre_install_callback(self._ensure_buckets)

    def _get_pkg_manager_installed(self) -> str | None:
        return shutil.which("scoop")

    def _get_supported_oses(self) -> set[str]:
        return {_PLATFORM_WINDOWS}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "iwr -useb get.scoop.sh | iex"
        ]

    def _post_install_pkg_manager(self) -> None:
        # update current PATH (current process path)
        scoop_shims = os.path.expandvars(r"%USERPROFILE%\scoop\shims")
        os.environ["PATH"] += os.pathsep + scoop_shims

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        pkg_mgr_bin = self._get_pkg_manager_installed()
        pkg_mgr_bin = pkg_mgr_bin if pkg_mgr_bin else "SCOOP_NOT_FOUND"
        return [pkg_mgr_bin, "install", dependency, "-k"]

    def _ensure_buckets(self):
        scoop_bin = self._get_pkg_manager_installed() or "SCOOP_NOT_FOUND"
        process = Environment.run(
            f"{scoop_bin}", "bucket", "list",
        )
        for bucket in self._buckets:
            if bucket in process.stdout:
                logger.info(f"{_('Skipping bucket')} '{bucket}'. {_('Already added in scoop')}.")
                continue
            logger.info(f"{_('Adding bucket')} '{bucket}' {_('to scoop')}.")
            Environment.run(
                f"{scoop_bin}", "bucket", "add", f"{bucket}",
            )
            logger.info(f"{_('Bucket')} '{bucket}' {_('added to scoop')}.")


__all__ = [
    "ScoopPackageManager",
]
