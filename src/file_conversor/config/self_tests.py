# src\file_conversor\config\self_tests.py

import sys

from pathlib import Path

# user provided imports
from file_conversor.config.environment import Environment
from file_conversor.config.log import Log
from file_conversor.config.locale import get_translation

# Get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class SelfTests:
    """ Manages application dependencies (internal and external). """

    __INTERNAL_DEPENDENCY_TRANSLATION = {
        "Babel": "babel",
        "pillow": "PIL",
        "pyyaml": "yaml",
        "concurrent-log-handler": "concurrent_log_handler",
        "requests-cache": "requests_cache",
        "pywin32": "win32api",
    }

    @classmethod
    def _get_internal_dependencies(cls) -> list[str]:
        """ Get the list of internal dependencies. """
        import toml
        import re

        pyproject_toml_path = Environment.get_resources_folder() / "pyproject.toml"
        if not pyproject_toml_path.exists():
            pyproject_toml_path = Path() / "pyproject.toml"
        PYPROJECT = toml.load(pyproject_toml_path)

        dependencies: list[str] = []
        for dep in PYPROJECT["project"]["dependencies"]:
            match = re.match(r"^[a-zA-Z0-9_\-]+", dep)
            if not match:
                raise RuntimeError(f"{_('Cannot parse dependency:')} '{dep}' {_('from pyproject.toml')}")
            package_name = match.group(0)  # Get the package name (before any version specifier)
            dependencies.append(package_name)
        return dependencies

    @classmethod
    def _should_skip_dependency_by_os(cls, dependency: str) -> bool:
        """ Determine if a dependency should be skipped based on the OS. """
        if any(x in dependency.lower() for x in ["win32"]) and sys.platform != "win32":
            return True
        if any(x in dependency.lower() for x in ["macos", "darwin"]) and sys.platform != "darwin":
            return True
        if any(x in dependency.lower() for x in ["linux"]) and sys.platform != "linux":
            return True
        return False

    @classmethod
    def _check_internal_dependencies(cls) -> Exception | None:
        """ Check for internal dependencies. """
        import importlib

        exception: Exception | None = None
        logger.info(f"  {_('Checking internal dependencies:')}")
        for dependency in cls._get_internal_dependencies():
            try:
                if cls._should_skip_dependency_by_os(dependency):
                    logger.warning(f"    [bold yellow]⚠[/]\t{dependency} (skipped on this platform)")
                    continue

                dependency = cls.__INTERNAL_DEPENDENCY_TRANSLATION.get(dependency, dependency)
                importlib.import_module(dependency)
                logger.info(f"    [bold green]OK[/]\t- {dependency}")
            except Exception as e:
                logger.info(f"    [bold red]FAIL[/]\t- {dependency}")
                exception = e

        if exception is not None:
            return RuntimeError(f"{_('Some dependencies are missing or cannot be imported. Please check the logs.')}")

    @classmethod
    def _check_external_dependencies(cls) -> Exception | None:
        """ Check for external dependencies. """
        logger.info(f"  {_('Checking external dependencies:')}")
        # xTODO: implement external dependency checks

    @classmethod
    def _run_pytest(cls) -> Exception | None:
        """ Run pytest to perform self-tests. """
        try:
            import pytest

            tests_path = Environment.get_resources_folder() / "tests"
            if not tests_path.exists():
                logger.warning(f" {_('Tests folder not found at')} '{tests_path}'. {_('Skipping pytest self-tests.')}")
                return

            result = pytest.main(["-v", "--tb=short", "--disable-warnings", str(tests_path)])
            if result != 0:
                return RuntimeError(f"{_('Some pytest self-tests have failed with exit-code')} {result}. {_('Please check the logs.')}")
        except ImportError:
            logger.warning(f"{_('pytest is not installed. Please install it to run self-tests.')}")

    @classmethod
    def run_self_tests(cls):
        """ Perform a app self-test. """
        logger.info(f"{_('Running application self-tests ...')}")
        exceptions: list[Exception | None] = [
            cls._check_internal_dependencies(),
            cls._check_external_dependencies(),
            cls._run_pytest(),
        ]
        for e in exceptions:
            if e is None:
                continue
            raise e
        logger.info(f"{_('Running application self-tests ...')} [bold green]OK[/]")


__all__ = [
    "SelfTests",
]
