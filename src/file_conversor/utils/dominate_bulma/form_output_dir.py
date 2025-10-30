# src\file_conversor\utils\bulma\form_output_dir.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_input import FormFieldInput

from file_conversor.utils.dominate_utils import *


def FormFieldOutputDirectory(
    help: str,
    _name: str,
    **kwargs,
):
    """
    Create a form field for selecting an output directory.

    :param help: Optional help text.
    :param _name: The name attribute for the select element.
    """
    return FormFieldInput(
        validation_expr="value.length > 0",
        _name=_name,
        help=help,
        button={
            "icon": {"name": "folder-open"},
            "_class": "is-info",
            "_title": help,
            "@click": "openFolderDialog",
        },
        x_data="""
            async openFolderDialog() {
                const folderList = await pywebview.api.open_folder_dialog({ });
                if (folderList && folderList.length > 0) {
                    this.value = folderList[0];
                }
            },
        """,
        **kwargs,
    )


__all__ = [
    "FormFieldOutputDirectory",
]
