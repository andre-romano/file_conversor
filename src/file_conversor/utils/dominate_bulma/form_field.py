# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon
from file_conversor.utils.dominate_utils import div, label, p

from file_conversor.utils.formatters import format_py_to_js


def _validate_func_js(validation_expr: str, value: str, is_valid_var: str) -> str:
    return f"""
        console.log('Validating field with value:', {value});
        {is_valid_var} = {validation_expr} ;
        const parentForm = this.$el.closest('form[x-data]');
        if(parentForm){{
            const parentData = Alpine.$data(parentForm);
            parentData.updateValidity();
        }} else {{
            console.log('No parent form found');
        }}
        return {is_valid_var} ;
    """


def _grouped_field(*input_el: Any, _class_control: str) -> list[Any]:
    controls = []
    for el in input_el:
        if not el:
            continue
        with div(_class=f"control {_class_control}") as control_group:
            control_group.add(el)
        controls.append(control_group)
    return controls


def _addons_field(*input_el: Any) -> list[Any]:
    with div(_class=f"field has-addons") as control_group:
        for el in input_el:
            if not el:
                continue
            control_group.add(el)
    return [control_group]


def _icon_component(icons: dict[str, Any], position: str) -> list[Any]:
    icon_fields = []
    if icons and icons.get(position):
        icon_fields.append(FontAwesomeIcon(icons[position], _class=f"is-{position} is-small"))
    return icon_fields


def _icons_field(*input_el: Any, icons: dict[str, Any], _class_control: str) -> list[Any]:
    _icons_class = ''
    _icons_class += 'has-icons-left' if icons.get('left') else ''
    _icons_class += 'has-icons-right' if icons.get('right') else ''
    with div(_class=f"control {_class_control}") as control:
        for el in input_el:
            if not el:
                continue
            control.add(el)
        control.add(*_icon_component(icons, 'left'))
        control.add(*_icon_component(icons, 'right'))
    return [control]


def _label_component(label_text: str) -> list[Any]:
    components = []
    if label_text:
        components.append(
            label(label_text, _class="label")
        )
    return components


def _help_component(help_var: str, is_hidden: str) -> list[Any]:
    return [
        p(
            _class=f"help is-danger",
            **{
                'x-text': f'{help_var}',
                ':class': f"""{{
                    'is-hidden': {is_hidden},
                }}""",
            },
        )  # Placeholder for error messages
    ]


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
                    {_validate_func_js(validation_expr, value="value", is_valid_var="this.isValid")}
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
        field.add(*_label_component(label_text))
        if "is-grouped" in _class:
            field.add(*_grouped_field(*input_el, _class_control=_class_control))
        elif has_addons:
            field.add(*_addons_field(*input_el))
        else:
            field.add(*_icons_field(*input_el, icons=icons or {}, _class_control=_class_control))
        field.add(*_help_component("help", is_hidden="isValid"))
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
            field_label.add(*_label_component(label_text))
        with div(_class=f"field-body {_class_body}") as field_body:
            field_body.add(*form_fields)
    return field


__all__ = [
    "FormFieldHorizontal",
    "FormField",
]
