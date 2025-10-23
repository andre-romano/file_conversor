# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon

from file_conversor.utils.dominate_utils import *


def Button(
    *content: Any,
    _class: str = "",
    _type: str = "button",
    **kwargs,
):
    """
    Create a button element.

    :param content: The content for the button. Can be a label, icon element, or other.
    :param _class: Additional CSS classes for the button.
    :param _type: The type attribute for the button.
    """
    return button(
        *[
            c
            for c in content
            if c is not None
        ],
        _class=f"button {_class}",
        _type=_type,
        **kwargs,
    )


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


def Select(
        *options: tuple[str, str],
        placeholder: str = "",
        _class: str = "",
        _class_container: str = "",
        **kwargs,
):
    """
    Create a select dropdown.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param placeholder: Placeholder text for the select dropdown.
    :param _class: Additional CSS classes for the select element.
    :param _class_container: Additional CSS classes for the select container.
    """
    with div(_class=f"select {_class_container}") as select_el:
        with select(_class=f"is-full-width {_class}", **kwargs,):
            if placeholder and not options:
                option(placeholder, _disabled=True, _selected=True, _hidden=True)
            for value, display_text in options:
                option(display_text, _value=value)
    return select_el


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


def FormField(
    *input_el,
    label_text: str = "",
    help: str = "",
    icons: dict[str, Any] | None = None,
    current_value: str | None = None,
    validation_expr: str = "true",
    has_addons: bool = False,
    _class: str = "",
    _class_control: str = "",
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
    """
    value = ""
    if current_value is None:
        value = "null"
    if current_value and current_value.lower() == "true":
        value = "true"
    elif current_value and current_value.lower() == "false":
        value = "false"
    else:
        value = current_value

    with div(
        _class=f"field is-full-width {_class}",
        **{
            'x-data': """{
                help: '%s',
                value: '%s',
                isValid: false,
                validate(value){
                    console.log('Validating field with value:', value);
                    this.isValid = %s ;
                    const parentForm = this.$el.closest('form[x-data]');
                    if(parentForm){
                        const parentData = Alpine.$data(parentForm);
                        parentData.updateValidity();
                    } else {
                        console.log('No parent form found');
                    }
                    return this.isValid ;
                },
                init() {
                    this.$watch('value', this.validate.bind(this));
                    this.validate(this.value);                    
                }
            }""" % (
                help,
                value,
                validation_expr,
            ),
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


def FormFieldRadio(
    *options: tuple[str, str],
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param _name: The name attribute for the select element.
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.

    :return: The FormField element.
    """
    field = FormField(
        *[
            Radio(
                _class="is-flex is-flex-grow-1",
                _name=_name,
                _value=value,
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
    )
    return field


def FormFieldCheckbox(
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param _name: The name attribute for the select element.
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.

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
    )
    return field


def FormFieldSelect(
    *options: tuple[str, str],
    current_value: str,
    help: str,
    _name: str,
    label_text: str = "",
    **kwargs,
):
    """
    Create a form field with a label and a select element.

    :param options: A list of tuples where each tuple contains (value, display_text).
    :param current_value: The current selected value.
    :param label_text: The text for the label.
    :param help: Optional help text.
    :param _name: The name attribute for the select element.

    :return: The FormField element.
    """
    field = FormField(
        Select(
            *options,
            _class="is-flex is-flex-grow-1",
            _name=_name,
            **{
                ':class': """{
                    'is-danger': !isValid,
                    'is-success': isValid,
                }""",
                'x-model': 'value',
                **kwargs,
            },
        ),
        current_value=current_value,
        _class_control="is-flex is-flex-direction-column is-flex-grow-1",
        label_text=label_text,
        help=help,
    )
    return field


def FormFieldInput(
    help: str,
    _name: str,
    _type: str = "text",
    current_value: str = "",
    label_text: str = "",
    validation_expr: str = "",
    button: dict[str, Any] | None = None,
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
    )
    return field


def FormFieldTextArea(
    _name: str,
    current_value: str,
    help: str,
    label_text: str = "",
    validation_expr: str = "",
    **kwargs,
):
    """
    Create a form field with a label and an input element.

    :param _name: The name attribute for the select element.
    :param current_value: The current value.
    :param help: Optional help text.
    :param label_text: The text for the label.
    :param validation_expr: The validation expression for the input.

    :return: The FormField element.
    """
    field = FormField(
        TextArea(
            _class="is-flex is-flex-grow-1",
            _name=_name,
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
    )
    return field


def FormFieldOutputDirectory(
    help: str,
    _name: str,
    **kwargs,
):
    """
    Create a form field for selecting an output directory.

    :param help: Optional help text.
    :param _name: The name attribute for the select element.
    """
    return FormFieldInput(
        validation_expr="value.length > 0",
        _name=_name,
        help=help,
        button={
            "icon": {"name": "folder-open"},
            "_class": "is-info",
            "@click": "Alpine.store('file_dialog').openFolderDialog",
        },
        **kwargs,
    )


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


def Form(
        *form_fields,
        _class: str = "",
        **kwargs,
):
    """
    Create a form element.

    :param form_fields: The form field elements (e.g., FormField).
    :param _class: Additional CSS classes for the form.
    :param kwargs: Additional attributes for the form element.
    """
    with form(_class=f"form {_class}", **kwargs) as form_elem:
        for form_field in form_fields:
            if not form_field:
                continue
            form_elem.add(form_field)
    return form_elem


__all__ = [
    "Form",
    "FormField",
    "FormFieldOutputDirectory",
    "FormFieldHorizontal",
    "FormFieldSelect",
    "FormFieldCheckbox",
    "FormFieldInput",
    "FormFieldTextArea",
    "FormFieldRadio",
    "Input",
    "Select",
    "TextArea",
    "Checkbox",
    "Radio",
    "Button",
]
