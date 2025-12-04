# src\file_conversor\utils\bulma\form_file_list.py

from typing import Any, Sequence

from file_conversor.utils.dominate_utils import button, div, i, input_, label, option, select, template, p
from file_conversor.utils.formatters import format_py_to_js


def _SelectBox(
        size: int = 8,
        _multiple: bool = True,
):
    """
    Create the select box for the file list.

    Needs alpine data with:
    - files: list of available files
    - selected: list of selected files
    - isValid: boolean indicating if the selection is valid

    :param size: The number of visible options in the select box.
    :param _multiple: Whether to allow multiple selection.

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
                _multiple=_multiple,
                _size=size,
                _class="is-full-width",
                _style="cursor: unset;",
                **{
                    "x-model": "selected",
                    ":title": "help",
                },
            ):
                with template(**{"x-for": "(opt, index) in files", ":key": "opt"}):
                    option(
                        **{
                            ":value": "opt",
                            "x-text": "`#${index + 1} - ${opt}`",
                        }
                    )
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
        up_help: str,
        down_help: str,
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

        with div(_class="is-flex"):
            # Upload button
            with button(
                _class="button is-success is-48x48 has-border",
                _title=add_help,
                **{
                    "@click.prevent": "openFileDialog"
                },
            ):
                i(_class="fa-solid fa-plus")
                input_(
                    _type="text",
                    _name=input_name,
                    _hidden=True,
                    **{
                        "x-model": "filesStr",
                    },
                )

            # Delete button
            with button(
                _class="button is-danger is-48x48 has-border ml-1",
                _title=remove_help,
                **{
                    "@click.prevent": """                
                        files = files.filter(file => !selected.includes(file));
                        selected = [];
                    """
                },
            ):
                i(_class="fa-solid fa-trash")

        # another set of buttons below
        with div(_class="is-flex mt-2"):
            # Up button
            with button(
                _class="button is-info is-48x48 has-border",
                _title=up_help,
                **{
                    "@click.prevent": """                
                        selected.forEach(file => {
                            const index = files.indexOf(file);
                            if (index > 0) {
                                // swap with the previous item
                                [files[index - 1], files[index]] = [files[index], files[index - 1]];
                            }
                        });
                        files = [...files]; // trigger reactivity
                    """
                },
            ):
                i(_class="fa-solid fa-arrow-up")

            # Down button
            with button(
                _class="button is-link is-outlined is-48x48 has-border ml-1",
                _title=down_help,
                **{
                    "@click.prevent": """                
                        selected.forEach(file => {
                            const index = files.indexOf(file);
                            if (index < files.length - 1) {
                                // swap with the next item
                                [files[index + 1], files[index]] = [files[index], files[index + 1]];
                                console.log('Moved down:', file);
                                console.log('Selected:', selected);
                            }
                        });
                        files = [...files]; // trigger reactivity
                    """
                },
            ):
                i(_class="fa-solid fa-arrow-down")

    return control_right


def FormFileList(
        label_text: str,
        input_name: str,
        validation_expr: str,
        multiple: bool = True,
        file_types: Sequence[str] | None = None,
        help_text: str = "",
        btn_add_help: str = "Add file",
        btn_remove_help: str = "Remove file",
        btn_up_help: str = "Move file up",
        btn_down_help: str = "Move file down",
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
                file_types: {format_py_to_js(file_types)},
                _validate_file(file) {{
                    if (this.file_types.length === 0) {{
                        return true; // no filter, accept all files
                    }}
                    const fileExt = file.split('.').pop().toLowerCase();
                    for (const type of this.file_types) {{
                        const file_types = type.split('(')[1].split(')')[0].split(';');
                        if (file_types.includes(`*.${{fileExt}}`) || file_types.includes(`*.*`)) {{
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
                    }});
                }},
                async openFileDialog() {{
                    const fileList = await pywebview.api.open_file_dialog({{                        
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
                    // watch alpine store 'drag_drop' for dropped files
                    this.$watch('$store.drag_drop.files', value => {{
                        this._updateFiles(value);
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
                    add_help=btn_add_help,
                    remove_help=btn_remove_help,
                    up_help=btn_up_help,
                    down_help=btn_down_help,
                )
            else:
                # Left-side controls
                _SelectButtons(
                    input_name=input_name,
                    add_help=btn_add_help,
                    remove_help=btn_remove_help,
                    up_help=btn_up_help,
                    down_help=btn_down_help,
                )
                # Right-side file list
                _SelectBox()
    return field


__all__ = [
    'FormFileList',
]
