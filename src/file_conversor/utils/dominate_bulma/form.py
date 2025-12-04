# src\file_conversor\utils\bulma\form.py

from typing import Any

from file_conversor.utils.dominate_bulma.font_awesome_icon import FontAwesomeIcon
from file_conversor.utils.dominate_utils import form


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
]
