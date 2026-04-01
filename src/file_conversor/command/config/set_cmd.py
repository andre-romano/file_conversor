
# src\file_conversor\command\config\set_cmd.py

from enum import StrEnum
from typing import override

# user-provided modules
from file_conversor.backend import (
    FFmpegBackend,
    GhostscriptBackend,
    Img2PDFBackend,
    PillowBackend,
)
from file_conversor.command.abstract_cmd import AbstractCommand
from file_conversor.config import (
    Configuration,
    ConfigurationData,
    Log,
    State,
    get_translation,
)


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

ConfigSetExternalDependencies: set[str] = set()  # no external dependencies, as this command is for setting configuration options


class ConfigSetInFormats(StrEnum):
    pass  # no input formats, as this command is for setting configuration options


class ConfigSetOutFormats(StrEnum):
    pass  # no output formats, as this command is for setting configuration options


ConfigSetVideoQuality = FFmpegBackend.VideoQuality
ConfigSetVideoEncoding = FFmpegBackend.VideoEncoding

ConfigSetVideoOutFormat = FFmpegBackend.SupportedOutVideoFormats
ConfigSetAudioOutFormat = FFmpegBackend.SupportedOutAudioFormats

ConfigSetImageFitMode = Img2PDFBackend.FitMode
ConfigSetImagePageLayout = Img2PDFBackend.PageLayout
ConfigSetImageResamplingOption = PillowBackend.ResamplingOption

ConfigSetPdfCompression = GhostscriptBackend.Compression


class ConfigSetCommand(AbstractCommand[ConfigSetInFormats, ConfigSetOutFormats], ConfigurationData):
    @classmethod
    @override
    def _external_dependencies(cls):
        return ConfigSetExternalDependencies

    @classmethod
    @override
    def _supported_in_formats(cls):
        return ConfigSetInFormats

    @classmethod
    @override
    def _supported_out_formats(cls):
        return ConfigSetOutFormats

    @override
    def execute(self):
        # update the configuration dictionary
        Configuration.set(self)
        Configuration.save()
        logger.info(f"{_('Configuration file updated')}")


__all__ = [
    "ConfigSetExternalDependencies",
    "ConfigSetInFormats",
    "ConfigSetOutFormats",

    "ConfigSetVideoQuality",
    "ConfigSetVideoEncoding",
    "ConfigSetVideoOutFormat",
    "ConfigSetAudioOutFormat",
    "ConfigSetImageFitMode",
    "ConfigSetImagePageLayout",
    "ConfigSetImageResamplingOption",
    "ConfigSetPdfCompression",

    "ConfigSetCommand",
]
