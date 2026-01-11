
# tests\backend\test_abstract_backend.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.dependency import AbstractPackageManager

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd

# unsupported OS


class _DummyPkgManagerUnsupportedOS(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] = {}) -> None:
        super().__init__(dependencies=dependencies)

    def _get_pkg_manager_installed(self) -> str | None:
        return None

    def _get_supported_oses(self) -> set[str]:
        return {"NonExistingOS123"}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    def _post_install_pkg_manager(self) -> None:
        """Empty on purpose for testing."""
        pass

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


class _DummyPkgManagerNotInstalled(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] = {}) -> None:
        super().__init__(dependencies=dependencies)

    def _get_pkg_manager_installed(self) -> str | None:
        return None

    def _get_supported_oses(self) -> set[str]:
        return {"DummyOS", platform.system()}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    def _post_install_pkg_manager(self) -> None:
        """Empty on purpose for testing."""
        pass

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


class _DummyPkgManager(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] = {}) -> None:
        super().__init__(dependencies=dependencies)

    def _get_pkg_manager_installed(self) -> str | None:
        return "dummy_pkg_manager"

    def _get_supported_oses(self) -> set[str]:
        return {"DummyOS", platform.system()}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    def _post_install_pkg_manager(self) -> None:
        """Empty on purpose for testing."""
        pass

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
class TestAbstractBackend:
    def test_find_in_path_not_exists(self):
        assert AbstractBackend.find_in_path("cmd.exe").exists()
        assert AbstractBackend.find_in_path("cmd").exists()
        with pytest.raises(FileNotFoundError):
            AbstractBackend.find_in_path("non_existing_executable_12345.exe")
        with pytest.raises(FileNotFoundError):
            AbstractBackend.find_in_path("test.json")

    def test_check_file_exists(self):
        existing_file = DATA_PATH / "test.json"
        non_existing_file = DATA_PATH / "non_existing_file.txt"

        # This should not raise an exception
        AbstractBackend.check_file_exists(existing_file)

        # This should raise a FileNotFoundError
        with pytest.raises(FileNotFoundError):
            AbstractBackend.check_file_exists(non_existing_file)

    def test_init_backend(self):
        backend = AbstractBackend()
        assert backend is not None

        backend_with_pkg = AbstractBackend(pkg_managers=set())
        assert backend_with_pkg is not None

        backend_with_pkg_and_path = AbstractBackend(
            pkg_managers={
                _DummyPkgManager()
            }, install_answer=True,
        )
        assert backend_with_pkg_and_path is not None

        with pytest.raises(RuntimeError):
            AbstractBackend(
                pkg_managers={
                    _DummyPkgManagerNotInstalled({
                        "cmd.exe": "dummy_dependency_1",
                        "another_non_existing_executable_67890.exe": "dummy_dependency_2",
                    })
                }, install_answer=True,
            )

        with pytest.raises(RuntimeError):
            AbstractBackend(
                pkg_managers={
                    _DummyPkgManagerNotInstalled({
                        "cmd.exe": "dummy_dependency_1",
                        "another_non_existing_executable_67890.exe": "dummy_dependency_2",
                    })
                }, install_answer=False,
            )

        # unsupported OS
        backend_with_pkg_and_path = AbstractBackend(
            pkg_managers={
                _DummyPkgManagerUnsupportedOS({
                    "cmd.exe": "dummy_dependency_1",
                    "another_non_existing_executable_67890.exe": "dummy_dependency_2",
                })
            }, install_answer=True,
        )
        assert backend_with_pkg_and_path is not None
