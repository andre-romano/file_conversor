# src\file_conversor\backend\gui\_components\modal.py

from file_conversor.utils.dominate_utils import *

from typing import Any


def ModalCard(
        *content: Any,
        _title: str,
        footer_content: Any = None,
        closeable: bool = True,
        _class_head: str = "",
        _class_body: str = "",
        _class_foot: str = "",
        **kwargs
):
    """
    Create a modal card component.

    :param _title: The title of the modal.
    :param content: The content to display inside the modal body.
    :param footer_content: The content to display inside the modal footer.
    :param closeable: Whether the modal can be closed by the user.
    :param _class_head: Additional CSS classes to apply to the modal header.
    :param _class_body: Additional CSS classes to apply to the modal body.
    :param _class_foot: Additional CSS classes to apply to the modal footer.
    """
    content_filtered = []
    for item in content:
        if not item:
            continue
        content_filtered.append(item)

    with div(
        _class="modal is-active",
        **kwargs,
    ) as modal:

        # Modal background
        div(_class="modal-background")

        # Modal card
        with div(_class="modal-card"):

            # Modal header
            with header(_class=f"modal-card-head {_class_head}"):
                p(_title, _class="modal-card-title")
                button(
                    _class=f"delete {'is-hidden' if not closeable else ''}",
                    _aria_label="close",
                    _onclick="document.querySelector('.modal.is-active').remove()",
                )

            # Modal body
            section(
                *content_filtered,
                _class=f"modal-card-body {_class_body}",
            )

            # Modal footer
            if footer_content:
                footer(
                    footer_content,
                    _class=f"modal-card-foot {_class_foot}",
                )
    return modal


def Modal(*content, **kwargs):
    """
    Create a simple modal component.

    :param content: The content to display inside the modal.
    """

    with div(
        _class="modal is-active",
        **kwargs,
    ) as modal:

        # Modal background
        div(_class="modal-background")

        # Modal content
        with div(_class="modal-content") as modal_body:
            for item in content:
                if not item:
                    continue
                modal_body.add(item)
    return modal


__all__ = [
    "ModalCard",
    "Modal",
]
