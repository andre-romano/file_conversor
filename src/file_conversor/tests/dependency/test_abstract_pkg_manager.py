
# tests\backend\test_abstract_pkg_manager.py

from pathlib import Path
from typing import override

import pytest

# user-provided imports
from file_conversor.dependency import AbstractPackageManager
from file_conversor.system.abstract_system import AbstractSystem


# unsupported OS
class _DummyPkgManagerUnsupportedOS(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] | None = None) -> None:
        super().__init__(dependencies=dependencies or {})

    @override
    def _get_pkg_manager_installed(self) -> str | None:
        """ empty on purpose for testing. """
        return None

    @override
    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        return {AbstractSystem.Platform.LINUX}

    @override
    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    @override
    def _post_install_pkg_manager(self) -> None:
        """ empty on purpose for testing. """

    @override
    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


class _DummyPkgManagerNotInstalled(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] | None = None) -> None:
        super().__init__(dependencies=dependencies or {})

    @override
    def _get_pkg_manager_installed(self) -> str | None:
        """ empty on purpose for testing. """
        return None

    @override
    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        return {AbstractSystem.Platform.get()}

    @override
    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    @override
    def _post_install_pkg_manager(self) -> None:
        """ empty on purpose for testing. """

    @override
    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


class _DummyPkgManager(AbstractPackageManager):
    def __init__(self, dependencies: dict[str, str] | None = None, env: list[str | Path] | None = None) -> None:
        super().__init__(dependencies=dependencies or {}, env=env or [])

    @override
    def _get_pkg_manager_installed(self) -> str | None:
        return "dummy_pkg_manager"

    @override
    def _get_supported_oses(self) -> set[AbstractSystem.Platform]:
        return {AbstractSystem.Platform.get()}

    @override
    def _get_cmd_install_pkg_manager(self) -> list[str]:
        return ["echo", "Installing dummy package manager..."]

    @override
    def _post_install_pkg_manager(self) -> None:
        """ empty on purpose for testing. """

    @override
    def _get_cmd_install_dep(self, dependency: str) -> list[str]:
        return ["echo", f"Installing dependency {dependency}..."]


@pytest.mark.skipif(AbstractSystem.Platform.get() != AbstractSystem.Platform.WINDOWS, reason="Windows-only test class")
class TestAbstractPkgManager:
    def test_check_dependencies(self):
        pkg_manager = _DummyPkgManager({
            "cmd.exe": "dummy_dependency_1",
            "another_non_existing_executable_67890.exe": "dummy_dependency_2",
        }, env=[
            "c:/Windows/System32/xxx",
            "c:/windows" if AbstractSystem.Platform.get() == AbstractSystem.Platform.WINDOWS else "/usr/bin",
        ])
        missing_deps = pkg_manager.get_missing_dependencies()
        if AbstractSystem.Platform.get() == AbstractSystem.Platform.WINDOWS:
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

    def test_get_supported_oses(self):
        pkg_manager = _DummyPkgManager()
        supported_oses = pkg_manager.get_supported_oses()
        assert AbstractSystem.Platform.get() in supported_oses

        pkg_manager_unsupported = _DummyPkgManagerUnsupportedOS()
        supported_oses_unsupported = pkg_manager_unsupported.get_supported_oses()
        assert AbstractSystem.Platform.get() not in supported_oses_unsupported

    def test_install_pkg_manager(self):
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
