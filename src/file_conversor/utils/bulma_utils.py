# src\file_conversor\utils\bulma_utils.py

from typing import Any

# user-provided modules
from file_conversor.utils.dominate_utils import *
from file_conversor.utils.dominate_bulma import *

from file_conversor.utils.formatters import format_file_types_webview

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def InputFilesField(
        *file_types: str,
        description: str = "",
):
    """
    Create a FormFieldInput for file list input.

    :param file_types: File type patterns (e.g., '.png', '.jpg').
    :param description: Description for the file types (e.g., 'Image Files').
    """
    return FormFileList(
        input_name="input-files",
        validation_expr="value.length > 0",
        label_text=_("Input Files"),
        help_text=_("Select (or drag) the input files."),
        add_help=_("Add file"),
        remove_help=_("Remove file"),
        file_types=[
            format_file_types_webview(
                *file_types,
                description=description,
            ),
        ],
        multiple=True,
    )


def OutputDirField():
    return FormFieldHorizontal(
        FormFieldOutputDirectory(
            _name="output-dir",
            help=_("Select the output directory to save the file."),
        ),
        label_text=_("Output Directory"),
    )


def FileFormatField(
    *options: tuple[str, str],
    current_value: str | None = None,
):
    """
    Create a form field for file format selection.

    :param options: A list of tuples where each tuple contains (value, display_text)
    :param current_value: The currently selected value.
    """
    return FormFieldHorizontal(
        FormFieldSelect(
            *options,
            current_value=current_value,
            _name="file-format",
            help=_("Select the output file format."),
        ),
        label_text=_("Output Format"),
    )


def OverwriteFilesField():
    """Create a form field for overwrite option."""
    return FormFieldCheckbox(
        current_value=STATE["overwrite-output"],
        _name="overwrite",
        label_text=_("Overwrite Existing Files"),
        help=_("Allow overwriting of existing files."),
    )


def AudioBitrateField():
    """Create a form field for audio bitrate input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0",
            current_value=CONFIG['audio-bitrate'],
            _name="audio-bitrate",
            _type="number",
            help=_("Set audio bitrate (in kbps). Type 0 to keep original audio bitrate."),
        ),
        label_text=_("Audio Bitrate (kbps)"),
    )


def VideoBitrateField():
    """Create a form field for video bitrate input."""
    return FormFieldHorizontal(
        FormFieldInput(
            validation_expr="Number.parseInt(value) >= 0",
            current_value=CONFIG['video-bitrate'],
            _name="video-bitrate",
            _type="number",
            help=_("Set video bitrate (in kbps). Type 0 to keep original video bitrate."),
        ),
        label_text=_("Video Bitrate (kbps)"),
    )


__all__ = [
    "InputFilesField",
    "OutputDirField",
    "FileFormatField",
    "OverwriteFilesField",
    "AudioBitrateField",
    "VideoBitrateField",
]
