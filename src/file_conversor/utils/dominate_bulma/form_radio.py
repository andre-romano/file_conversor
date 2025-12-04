# src\file_conversor\utils\bulma\form_radio.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_field import FormField
from file_conversor.utils.dominate_utils import input_, label, span


def Radio(
    label_text: str,
    _name: str,
    _value: str,
    _class: str = "",
    **kwargs,
):
    """
    Create a radio input.

    :param label_text: The text for the radio label.
    :param _name: The name attribute for the radio input.
    :param _value: The value attribute for the radio input.
    :param _class: Additional CSS classes for the radio.
    """
    with label(_class=f"radio {_class}") as radio_label:
        input_(_type="radio", _name=_name, _value=_value, **kwargs)
        span(label_text)
    return radio_label


def FormFieldRadio(
    *options: tuple[str, str],
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param _name: The name attribute for the select element.
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.
    :param x_data: Additional Alpine.js x-data properties.

    :return: The FormField element.
    """
    field = FormField(
        *[
            Radio(
                _class="is-flex is-flex-grow-1",
                _name=_name,
                _value=value,
                _title=help,
                label_text=display_text,
                **{
                    ':class': """{
                        'is-danger': !isValid,
                        'is-success': isValid,
                    }""",
                    'x-model': 'value',
                },
                **kwargs,
            )
            for value, display_text in options
        ],
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        current_value=current_value,
        label_text=label_text,
        help=help,
        x_data=x_data,
        x_init=x_init,
    )
    return field


__all__ = [
    "Radio",
    "FormFieldRadio",
]
