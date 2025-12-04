# src\file_conversor\utils\bulma\form_output_file.py

import os

from pathlib import Path
from typing import Any, Sequence

from file_conversor.utils.dominate_bulma.form_input import FormFieldInput

from file_conversor.utils.formatters import format_py_to_js


def FormFieldOutputFile(
    help: str,
    _name: str,
    file_types: Sequence[str],
    _readonly: bool = False,
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field for selecting an output file.

    :param help: Optional help text.
    :param _name: The name attribute for the select element.
    :param file_types: List of accepted file types (e.g., ['.pdf', '.docx']).
    :param _readonly: Whether the input field is read-only.
    :param x_data: Additional x-data for the component.
    :param x_init: Additional x-init for the component.
    """
    return FormFieldInput(
        validation_expr="value.length > 0",
        _readonly=_readonly,
        _name=_name,
        help=help,
        button={
            "icon": {"name": "file-export"},
            "_class": "ml-2 is-info",
            "_title": help,
            "@click": "saveFileDialog",
        },
        x_data=f"""            
            async saveFileDialog() {{
                const fileList = await pywebview.api.save_file_dialog({{                    
                    filename: this.value,
                    file_types: {format_py_to_js(file_types)},
                }});
                console.log('Save file dialog returned:', fileList);
                if (fileList && fileList.length > 0) {{
                    this.value = fileList[0];
                }}
            }},
            {x_data}
        """,
        x_init=f"""
            let thisObj = this;
            windowEventHandler.on('pywebviewready', async () => {{
                const dir = await pywebview.api.get_last_open_dir();
                if (thisObj.value && thisObj.value !== '') {{
                    thisObj.value = dir + '{os.sep if os.sep == '/' else r'\\'}' + thisObj.value;
                }}
            }});
            {x_init}
        """,
        **kwargs,
    )


__all__ = [
    "FormFieldOutputFile",
]
