# src\file_conversor\utils\bulma\form_output_file.py

from pathlib import Path
from typing import Any, Sequence

from file_conversor.utils.dominate_bulma.form_input import FormFieldInput

from file_conversor.utils.dominate_utils import *

from file_conversor.utils.formatters import format_py_to_js


def FormFieldOutputFile(
    help: str,
    _name: str,
    file_types: Sequence[str],
    path: str | Path = "",
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field for selecting an output file.

    :param help: Optional help text.
    :param _name: The name attribute for the select element.
    :param file_types: List of accepted file types (e.g., ['.pdf', '.docx']).
    :param path: Initial path for the file dialog.
    :param x_data: Additional x-data for the component.
    :param x_init: Additional x-init for the component.
    """
    return FormFieldInput(
        validation_expr="value.length > 0",
        _name=_name,
        help=help,
        button={
            "icon": {"name": "file-export"},
            "_class": "is-info",
            "_title": help,
            "@click": "saveFileDialog",
        },
        x_data=f"""
            lastPath: {format_py_to_js(path)},
            async updateLastPath(path) {{
                const lastSeen = path.lastIndexOf(`/`);
                const lastSeenWin = path.lastIndexOf(`\\\\`);
                this.lastPath = path.substring(0, Math.max(lastSeen, lastSeenWin) + 1);
            }},
            async saveFileDialog() {{
                const fileList = await pywebview.api.save_file_dialog({{
                    path: this.lastPath,
                    filename: this.value,
                    file_types: {format_py_to_js(file_types)},
                }});
                console.log('Save file dialog returned:', fileList);
                if (fileList && fileList.length > 0) {{
                    this.value = fileList[0];
                    this.updateLastPath(fileList[0]);
                }}
            }},
            {x_data}
        """,
        x_init=x_init,
        **kwargs,
    )


__all__ = [
    "FormFieldOutputFile",
]
