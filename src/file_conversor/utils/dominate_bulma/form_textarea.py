# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_field import FormField
from file_conversor.utils.dominate_utils import textarea


def TextArea(
    _class: str = "",
    **kwargs,
):
    """
    Create a textarea element.

    :param _class: Additional CSS classes for the textarea.
    """
    return textarea(
        _class=f"textarea {_class}",
        **kwargs,
    )


def FormFieldTextArea(
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    validation_expr: str = "",
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and an input element.

    :param _name: The name attribute for the select element.
    :param current_value: The current value.
    :param help: Optional help text.
    :param label_text: The text for the label.
    :param validation_expr: The validation expression for the input.
    :param x_data: Additional Alpine.js x-data properties.

    :return: The FormField element.
    """
    field = FormField(
        TextArea(
            _class="is-flex is-flex-grow-1",
            _name=_name,
            _title=help,
            **{
                ':class': """{
                    'is-danger': !isValid,
                    'is-success': isValid,
                }""",
                'x-model': 'value',
                **kwargs,
            }
        ),
        current_value=current_value,
        validation_expr=validation_expr,
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        label_text=label_text,
        help=help,
        x_data=x_data,
        x_init=x_init,
    )
    return field


__all__ = [
    "TextArea",
    "FormFieldTextArea",
]
