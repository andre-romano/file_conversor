
# src\file_conversor\command\config\show_cmd.py

from enum import StrEnum
from typing import override

# user-provided modules
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import CONFIG, LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


ConfigShowExternalDependencies: set[str] = set()  # no external dependencies, as this command is for setting configuration options


class ConfigShowInFormats(StrEnum):
    pass  # no input formats, as this command is for setting configuration options


class ConfigShowOutFormats(StrEnum):
    pass  # no output formats, as this command is for setting configuration options


class ConfigShowCommand(AbstractCommand[ConfigShowInFormats, ConfigShowOutFormats]):
    @classmethod
    @override
    def _external_dependencies(cls):
        return ConfigShowExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ConfigShowInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ConfigShowOutFormats

    @override
    def execute(self):
        logger.info(f"{_('Configuration')}: {CONFIG.to_dict()}")


__all__ = [
    "ConfigShowCommand",
]
