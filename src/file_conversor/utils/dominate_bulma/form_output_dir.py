# src\file_conversor\utils\bulma\form_output_dir.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_input import FormFieldInput


def FormFieldOutputDirectory(
    help: str,
    _name: str,
    _readonly: bool = False,
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field for selecting an output directory.

    :param help: Optional help text.
    :param _name: The name attribute for the select element.
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
            "icon": {"name": "folder-open"},
            "_class": "ml-2 is-info",
            "_title": help,
            "@click": "openFolderDialog",
        },
        x_data=f"""
            async openFolderDialog() {{
                const folderList = await pywebview.api.open_folder_dialog({{ }});
                if (folderList && folderList.length > 0) {{
                    this.value = folderList[0];
                }}
            }},
            {x_data}
        """,
        x_init=f"""
            let thisObj = this;
            windowEventHandler.on('pywebviewready', async () => {{
                thisObj.value = await pywebview.api.get_last_open_dir();
            }});
            {x_init}
        """,
        **kwargs,
    )


__all__ = [
    "FormFieldOutputDirectory",
]
