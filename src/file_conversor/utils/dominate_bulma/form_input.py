# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon

from file_conversor.utils.dominate_bulma.form_button import Button
from file_conversor.utils.dominate_bulma.form_field import FormField

from file_conversor.utils.dominate_utils import input_


def Input(
    _type: str = "text",
    _class: str = "",
    **kwargs,
):
    """
    Create an input element.

    :param _type: The type of the input (e.g., text, password, email).
    :param _class: Additional CSS classes for the input.
    """
    return input_(
        _type=_type,
        _class=f"input {_class}",
        **kwargs,
    )


def FormFieldInput(
    help: str,
    _name: str,
    _type: str = "text",
    current_value: str = "",
    label_text: str = "",
    validation_expr: str = "true",
    button: dict[str, Any] | None = None,
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and an input element.

    :param _name: The name attribute for the select element.
    :param _type: The type of the input (e.g., text, password, email).
    :param current_value: The current value.
    :param help: Optional help text.
    :param label_text: The text for the label.
    :param validation_expr: The validation expression for the input.
    :param button: Optional button to include next to the input. {"text": "Click Me", "_class": "button-class", "icon": {"name": "search"}}.

    :return: The FormField element.
    """
    field = FormField(
        Input(
            _class="is-flex is-flex-grow-1",
            _name=_name,
            _type=_type,
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
        Button(
            FontAwesomeIcon(**button.get('icon', {})),
            **{
                k: v
                for k, v in button.items()
                if k not in ['icon']
            },
        ) if button else None,
        has_addons=True if button else False,
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        current_value=current_value,
        validation_expr=validation_expr,
        label_text=label_text,
        help=help,
        x_data=x_data,
        x_init=x_init,
    )
    return field


__all__ = [
    "Input",
    "FormFieldInput",
]
