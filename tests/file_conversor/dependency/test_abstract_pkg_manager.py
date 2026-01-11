
# tests\backend\test_abstract_pkg_manager.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.dependency import *
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
        pass

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


class _DummyPkgManager(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] = {}, env: list[str | Path] = []) -> None:
        super().__init__(dependencies=dependencies, env=env)

    def _get_pkg_manager_installed(self) -> str | None:
        return "dummy_pkg_manager"

    def _get_supported_oses(self) -> set[str]:
        return {"DummyOS", platform.system()}

    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    def _post_install_pkg_manager(self) -> None:
        pass

    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-only test class")
class TestAbstractPkgManager:
    def test_check_dependencies(self):
        pkg_manager = _DummyPkgManager({
            "cmd.exe": "dummy_dependency_1",
            "another_non_existing_executable_67890.exe": "dummy_dependency_2",
        }, env=[
            "c:/Windows/System32/xxx",
            "c:/windows" if platform.system() == "Windows" else "/usr/bin",
        ])
        missing_deps = pkg_manager.check_dependencies()
        if platform.system() == "Windows":
            assert "dummy_dependency_1" not in missing_deps
            assert "dummy_dependency_2" in missing_deps
            assert len(missing_deps) == 1
        else:
            assert "dummy_dependency_1" in missing_deps
            assert "dummy_dependency_2" in missing_deps
            assert len(missing_deps) == 2

    def test_get_pkg_manager_installed(self):
        # installed
        pkg_manager_installed = _DummyPkgManager({
            "cmd.exe": "dummy_dependency_1",
            "another_non_existing_executable_67890.exe": "dummy_dependency_2",
        })
        pkg_mgr_path = pkg_manager_installed.get_pkg_manager_installed()
        assert pkg_mgr_path == "dummy_pkg_manager"

        # not installed
        pkg_manager_not_installed = _DummyPkgManagerUnsupportedOS()
        with pytest.raises(RuntimeError):
            pkg_mgr_path = pkg_manager_not_installed.get_pkg_manager_installed()

    def test_get_supported_oses(self):
        pkg_manager = _DummyPkgManager()
        supported_oses = pkg_manager.get_supported_oses()
        assert platform.system() in supported_oses

        pkg_manager_unsupported = _DummyPkgManagerUnsupportedOS()
        supported_oses_unsupported = pkg_manager_unsupported.get_supported_oses()
        assert platform.system() not in supported_oses_unsupported

    def test_install_pkg_manager(self):
        # pkg manager already installed (raise RuntimeError)
        pkg_manager_installed = _DummyPkgManager()
        with pytest.raises(RuntimeError):
            pkg_mgr_path = pkg_manager_installed.install_pkg_manager()

        # not installed (return None as shutil.which() cannot find dummy pkg manager)
        pkg_manager_not_installed = _DummyPkgManagerNotInstalled()
        pkg_mgr_path = pkg_manager_not_installed.install_pkg_manager()
        assert pkg_mgr_path == None

    def test_install_dependency(self):
        pkg_manager = _DummyPkgManagerNotInstalled({
            "cmd.exe": "dummy_dependency_1",
            "another_non_existing_executable_67890.exe": "dummy_dependency_2",
        })
        pkg_manager.add_pre_install_callback(lambda: print("Pre-install callback executed"))
        pkg_manager.add_post_install_callback(lambda: print("Post-install callback executed"))
        with pytest.raises(RuntimeError):
            pkg_manager.install_dependencies(["dummy_dependency_1"])

        pkg_manager_installed = _DummyPkgManager({
            "cmd.exe": "dummy_dependency_1",
            "another_non_existing_executable_67890.exe": "dummy_dependency_2",
        })
        pkg_manager_installed.add_pre_install_callback(lambda: print("Pre-install callback executed"))
        pkg_manager_installed.add_post_install_callback(lambda: print("Post-install callback executed"))
        pkg_manager_installed.install_dependencies(["dummy_dependency_1"])
