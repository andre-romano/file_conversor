# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.form_field import FormField
from file_conversor.utils.dominate_utils import div, option, select


def Select(
        *options: tuple[str, str],
        placeholder: str = "",
        _class: str = "",
        _class_container: str = "",
        kwargs_container: dict[str, Any] | None = None,
        **kwargs,
):
    """
    Create a select dropdown.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param placeholder: Placeholder text for the select dropdown.
    :param _class: Additional CSS classes for the select element.
    :param _class_container: Additional CSS classes for the select container.
    """
    with div(_class=f"select {_class_container}", **(kwargs_container if kwargs_container else {})) as select_el:
        with select(_class=f"is-full-width {_class}", **kwargs,):
            if placeholder and not options:
                option(placeholder, _disabled=True, _selected=True, _hidden=True)
            for value, display_text in options:
                option(display_text, _value=value)
    return select_el


def FormFieldSelect(
    *options: tuple[str, str],
    help: str,
    _name: str,
    label_text: str = "",
    current_value: str | None = None,
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.
    :param _name: The name attribute for the select element.
    :param x_data: Additional Alpine.js x-data properties.

    :return: The FormField element.
    """
    field = FormField(
        Select(
            *options,
            _class="is-flex is-flex-grow-1",
            _name=_name,
            _title=help,
            kwargs_container={
                ':class': """{
                    'is-danger': !isValid,
                    'is-success': isValid,
                }""",
            },
            **{'x-model': 'value'},
            **kwargs,
        ),
        current_value=current_value,
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        label_text=label_text,
        help=help,
        x_data=x_data,
        x_init=x_init,
    )
    return field


__all__ = [
    "Select",
    "FormFieldSelect",
]
