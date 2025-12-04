# src\file_conversor\utils\bulma\form_checkbox.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_field import FormField
from file_conversor.utils.dominate_utils import input_, label, span


def Checkbox(
    label_text: str,
    _class_container: str = "",
    _class_span: str = "",
    reverse: bool = False,
    **kwargs,
):
    """
    Create a checkbox input.

    :param label_text: The text for the checkbox label.
    :param _class_container: Additional CSS classes for the label container.
    :param _class_span: Additional CSS classes for the span containing the label text.
    :param reverse: Whether to reverse the order of the checkbox and label.    
    """
    with label(_class=f"checkbox {_class_container}") as checkbox_label:
        if reverse:
            span(label_text, _class=_class_span)
        input_(_type=f"checkbox", **kwargs)
        if not reverse:
            span(label_text, _class=_class_span)
    return checkbox_label


def FormFieldCheckbox(
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    reverse: bool = False,
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param _name: The name attribute for the select element.
    :param current_value: The current selected value.
    :param help: Optional help text.
    :param label_text: The text for the label.
    :param reverse: Whether to reverse the order of the checkbox and label.
    :param x_data: Additional Alpine.js x-data properties.
    :param x_init: Additional Alpine.js x-init script.

    :return: The FormField element.
    """
    field = FormField(
        Checkbox(
            label_text=label_text,
            _class_container=f"""
                is-flex 
                is-justify-content-flex-end 
                is-align-items-center
            """,
            _class=f"{'ml-1' if reverse else 'mr-1'}",
            _style="margin-top: 3px;",
            _name=_name,
            _title=help,
            reverse=reverse,
            **{
                ':class': """{
                    'is-danger': !isValid,
                    'is-success': isValid,
                }""",
                'x-model': 'value',
            },
            **kwargs,
        ),
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        current_value=True if current_value in ["true", "on", "yes", True] else False,
        help=help,
        x_data=x_data,
        x_init=x_init,
    )
    return field


__all__ = [
    "Checkbox",
    "FormFieldCheckbox",
]
