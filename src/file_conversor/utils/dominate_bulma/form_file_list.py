# src\file_conversor\utils\bulma\form_file_list.py

from typing import Any, Sequence

from file_conversor.utils.dominate_utils import *
from file_conversor.utils.formatters import format_py_to_js


def _SelectBox():
    """
    Create the select box for the file list.

    Needs alpine data with:
    - files: list of available files
    - selected: list of selected files
    - isValid: boolean indicating if the selection is valid

    :return: The select box element.
    """
    # Select box
    with div(_class="control is-flex is-flex-direction-column is-flex-grow-1") as control_left:
        with div(
            _class="select is-multiple is-flex is-flex-grow-1",
            **{
                ":class": """{
                        'is-danger': !isValid,
                        'is-success': isValid,
                    }""",
            },
        ):
            with select(
                _multiple=True,
                _size="8",
                _class="is-flex-grow-1",
                _style="cursor: unset;",
                **{
                    "x-model": "selected",
                    ":title": "help",
                },
            ):
                with template(**{"x-for": "opt in files"}):
                    option(**{":value": "opt", "x-text": "opt"})
        p(
            _class="help",
            **{
                ":class": """{
                    'is-danger': !isValid,
                    'is-hidden': isValid,
                }""",
                "x-text": "help",
            },
        )
    return control_left


def _SelectButtons(
        input_name: str,
        add_help: str,
        remove_help: str,
):
    """
    Create the select buttons for the file list.

    Needs alpine data with:
    - files: list of available files
    - filesStr: JSON string of the files
    - selected: list of selected files
    - isValid: boolean indicating if the selection is valid

    :return: The select buttons element.
    """
    with div(
        _class="control is-flex is-flex-direction-column is-justify-content-flex-start is-align-items-start ml-2"
    ) as control_right:

        # Upload button
        with div(_class="is-48x48 mb-2"):
            input_(
                _type="text",
                _name=input_name,
                _hidden=True,
                **{
                    "x-model": "filesStr",
                },
            )
            with button(
                _class="button is-info is-48x48 has-border",
                _title=add_help,
                **{
                    "@click.prevent": "openFileDialog"
                },
            ):
                i(_class="fa-solid fa-plus")

        # Delete button
        with button(
            _class="button is-danger is-48x48 has-border",
            _title=remove_help,
            **{
                "@click.prevent": """                
                    files = files.filter(file => !selected.includes(file));
                    selected = [];
                """
            },
        ):
            i(_class="fa-solid fa-trash")

    return control_right


def FormFileList(
        label_text: str,
        input_name: str,
        validation_expr: str,
        multiple: bool = True,
        file_types: Sequence[str] | None = None,
        help_text: str = "",
        add_help: str = "Add file",
        remove_help: str = "Remove file",
        reverse: bool = False,
):
    """
    Create a file list form field with select and buttons.

    :param label_text: The label text for the field.
    :param input_name: The name attribute for the hidden input field.
    :param validation_expr: The expression to validate the selection.
    :param multiple: Whether to allow multiple file selection.
    :param file_types: The file types to filter in the file dialog. Format "description (*.<extension;*.extension;...)".
    :param help_text: The help text for the field.
    :param reverse: Whether to reverse the order of buttons and select box.

    :return: The form field element.
    """
    with div(
        cls="field is-horizontal is-full-width",
        **{
            "x-data": f"""{{     
                selected: [],
                help: `{help_text}`,
                filesStr: '',
                files: [],
                isValid: false,
                lastPath: '',            
                file_types: {format_py_to_js(file_types)},
                _validate_file(file) {{
                    if (this.file_types.length === 0) {{
                        return true; // no filter, accept all files
                    }}
                    const fileExt = file.split('.').pop().toLowerCase();
                    for (const type of this.file_types) {{
                        const file_types = type.split('(')[1].split(')')[0].split(';');
                        if (file_types.includes(`*.` + fileExt)) {{
                            return true;
                        }}
                    }}
                    return false;
                }},
                _updateFiles(newFiles) {{
                    // extend files list, if newFiles is not already present
                    newFiles.forEach(file => {{
                        if (!this.files.includes(file) && this._validate_file(file)) {{
                            this.files.push(file);
                        }}
                        // get last path, for windows and unix compatibility
                        const lastSeen = file.lastIndexOf(`/`);
                        const lastSeenWin = file.lastIndexOf(`\\\\`);
                        this.lastPath = file.substring(0, Math.max(lastSeen, lastSeenWin) + 1);
                    }});
                }},
                async openFileDialog() {{
                    const fileList = await pywebview.api.open_file_dialog({{
                        path: this.lastPath,
                        multiple: {format_py_to_js(multiple)},
                        file_types: this.file_types,
                    }});
                    this._updateFiles(fileList);
                }},
                init() {{
                    this.$watch('files', value => {{     
                        this.filesStr = JSON.stringify(value);

                        this.isValid = {validation_expr};
                        const parentForm = this.$el.closest('form[x-data]');
                        if(parentForm){{
                            const parentData = Alpine.$data(parentForm);
                            parentData.updateValidity();
                        }} else {{
                            console.log('No parent form found');
                        }}
                    }});   
                    // Listen for filesDropped event
                    window.addEventListener('filesDropped', async (event) => {{
                        this._updateFiles(event.detail.files);
                        this.$nextTick(() => {{ }});
                    }});
                }},
            }}"""
        },
    ) as field:
        # Field label
        with div(_class="field-label"):
            label(label_text, _class="label")

        # Field body
        with div(_class="field-body is-flex is-flex-grow-5"):
            if not reverse:
                # Left-side file list
                _SelectBox()
                # Right-side controls
                _SelectButtons(
                    input_name=input_name,
                    add_help=add_help,
                    remove_help=remove_help,
                )
            else:
                # Left-side controls
                _SelectButtons(
                    input_name=input_name,
                    add_help=add_help,
                    remove_help=remove_help,
                )
                # Right-side file list
                _SelectBox()
    return field


__all__ = [
    'FormFileList',
]
