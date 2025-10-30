# src\file_conversor\utils\bulma\form_checkbox.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon

from file_conversor.utils.dominate_bulma.form_field import FormField

from file_conversor.utils.dominate_utils import *


def Checkbox(
    label_text: str,
    _class: str = "",
    _input: dict[str, Any] | None = None,
    **kwargs,
):
    """
    Create a checkbox input.

    :param label_text: The text for the checkbox label.
    :param _class: Additional CSS classes for the checkbox.
    """
    with label(_class=f"checkbox {_class}") as checkbox_label:
        input_(_type=f"checkbox", **_input if _input else {}, **kwargs)
        span(label_text)
    return checkbox_label


def FormFieldCheckbox(
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    x_data: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param _name: The name attribute for the select element.
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.
    :param x_data: Additional Alpine.js x-data properties.

    :return: The FormField element.
    """
    field = FormField(
        Checkbox(
            label_text=label_text,
            _class="is-flex is-justify-content-flex-end is-align-items-center",
            _input={
                '_class': "mr-1",
                "_style": "margin-top: 3px;",
            },
            _name=_name,
            _title=help,
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
        current_value=current_value,
        help=help,
        x_data=x_data,
    )
    return field


__all__ = [
    "Checkbox",
    "FormFieldCheckbox",
]
