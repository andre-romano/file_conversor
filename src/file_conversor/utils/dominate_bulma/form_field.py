# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon
from file_conversor.utils.dominate_utils import *

from file_conversor.utils.formatters import format_py_to_js


def FormField(
    *input_el,
    label_text: str = "",
    help: str = "",
    icons: dict[str, Any] | None = None,
    current_value: Any = None,
    validation_expr: str = "true",
    has_addons: bool = False,
    _class: str = "",
    _class_control: str = "",
    x_data: str = "",
    x_init: str = "",
    **kwargs,
):
    """
    Create a form field with a label and optional icons.

    :param input_el: The input elements (e.g., input, textarea, select).
    :param label_text: The text for the label.
    :param help: Optional help text.
    :param icons: Optional icons for left and right (e.g., {"left": left_icon_name, "right": right_icon_name}).
    :param _class: Additional CSS classes for the form field.
    :param _class_control: Additional CSS classes for the control div.
    :param x_data: Additional Alpine.js x-data properties.
    :param x_init: Additional Alpine.js x-init code.
    """
    with div(
        _class=f"field is-full-width {_class}",
        **{
            'x-data': f"""{{
                help: {format_py_to_js(help)},
                value: {format_py_to_js(current_value)},
                isValid: false,
                validate(value){{
                    console.log('Validating field with value:', value);
                    this.isValid = {validation_expr} ;
                    const parentForm = this.$el.closest('form[x-data]');
                    if(parentForm){{
                        const parentData = Alpine.$data(parentForm);
                        parentData.updateValidity();
                    }} else {{
                        console.log('No parent form found');
                    }}
                    return this.isValid ;
                }},
                init() {{
                    this.$watch('value', this.validate.bind(this));
                    this.validate(this.value);   
                    {x_init} ;                 
                }},
                {x_data}
            }}""",
        },
        **kwargs,
    ) as field:
        if label_text:
            label(label_text, _class="label")
        if "is-grouped" in _class:
            for el in input_el:
                if not el:
                    continue
                with div(_class=f"control {_class_control}") as control_group:
                    control_group.add(el)
        elif has_addons:
            with div(_class=f"field has-addons") as control_group:
                for el in input_el:
                    if not el:
                        continue
                    control_group.add(el)
        else:
            with div(_class=f"control {'has-icons-left' if icons and icons.get('left') else ''} {'has-icons-right' if icons and icons.get('right') else ''} {_class_control}") as control:
                for el in input_el:
                    if not el:
                        continue
                    control.add(el)
                if icons and icons.get('left'):
                    FontAwesomeIcon(icons['left'], _class="is-left is-small")
                if icons and icons.get('right'):
                    FontAwesomeIcon(icons['right'], _class="is-right is-small")
        p(
            _class=f"help is-danger",
            **{
                'x-text': 'help',
                ':class': """{
                    'is-hidden': isValid,
                }""",
            },
        )  # Placeholder for error messages
    return field


def FormFieldHorizontal(
    *form_fields,
    label_text: str,
    _class: str = "",
    _class_label: str = "is-normal",
    _class_body: str = "",
    **kwargs,
):
    """
    Create a horizontal form field with a label and multiple input elements.

    :param form_fields: The form field elements (e.g., FormField).
    :param label_text: The text for the label.
    :param _class: Additional CSS classes for the form field.
    :param _class_label: Additional CSS classes for the label container.
    :param _class_body: Additional CSS classes for the body container.
    :param kwargs: Additional attributes for the field container.
    """
    with div(_class=f"field is-horizontal is-full-width {_class}", **kwargs) as field:
        with div(_class=f"field-label {_class_label}") as field_label:
            label(label_text, _class="label")
        with div(_class=f"field-body {_class_body}") as field_body:
            for form_field in form_fields:
                field_body.add(form_field)
    return field


__all__ = [
    "FormFieldHorizontal",
    "FormField",
]
