# src\file_conversor\utils\bulma_utils\general.py

from pathlib import Path
from typing import Any, Sequence

# user-provided modules
from file_conversor.utils.dominate_bulma.form_field import FormFieldHorizontal
from file_conversor.utils.dominate_bulma.form_select import FormFieldSelect
from file_conversor.utils.dominate_bulma.form_checkbox import FormFieldCheckbox
from file_conversor.utils.dominate_bulma.form_file_list import FormFileList
from file_conversor.utils.dominate_bulma.form_output_dir import FormFieldOutputDirectory
from file_conversor.utils.dominate_bulma.form_output_file import FormFieldOutputFile

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
        btn_add_help=_("Add file"),
        btn_remove_help=_("Remove file"),
        file_types=[
            format_file_types_webview(
                *file_types,
                description=description,
            ),
        ],
        multiple=True,
    )


def OutputDirField(
    _name: str = "output-dir",
    help: str = _("Select the output directory to save the file."),
    label_text: str = _("Output Directory"),
):
    return FormFieldHorizontal(
        FormFieldOutputDirectory(
            _name=_name,
            help=help,
        ),
        label_text=label_text,
    )


def OutputFileField(
    *file_types: tuple[str, str],
    current_value: str = "",
):
    """
    Create a FormFieldOutputFile for selecting output file.

    :param file_types: A list of tuples with format (file_type, description).
    :param current_value: The current output filename. If provided, it will be appended to the last opened directory.
    """
    return FormFieldHorizontal(
        FormFieldOutputFile(
            _name="output-file",
            help=_("Select the output filename to save the file."),
            file_types=[
                format_file_types_webview(
                    ftype,
                    description=desc,
                ) for ftype, desc in file_types
            ],
            current_value=current_value,
        ),
        label_text=_("Output File"),
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
        _name="overwrite-output",
        label_text=_("Overwrite Existing Files"),
        help=_("Allow overwriting of existing files."),
    )


__all__ = [
    "InputFilesField",
    "OutputDirField",
    "OutputFileField",
    "FileFormatField",
    "OverwriteFilesField",
]
