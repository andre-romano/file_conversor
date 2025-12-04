# src\file_conversor\backend\gui\_components\modal.py

from typing import Any

# user-defined imports
from file_conversor.utils.dominate_utils import button, div, header, p, section, footer


def _Modal(**kwargs):
    with div(
        _class="modal",
        **{
            ":class": "{ 'is-active': $store.modal.show }",
            "x-data": "{ }",
        },
        **kwargs,
    ) as modal:

        # Modal background
        div(_class="modal-background")
    return modal


def ModalCard(
        _class_head: str = "",
        _class_body: str = "",
        _class_foot: str = "",
        kwargs_head: dict[str, Any] = {},
        kwargs_body: dict[str, Any] = {},
        kwargs_footer: dict[str, Any] = {},
        **kwargs,
):
    """
    Create a modal card component.

    :param _class_head: Additional CSS classes to apply to the modal header.
    :param _class_body: Additional CSS classes to apply to the modal body.
    :param _class_foot: Additional CSS classes to apply to the modal footer.
    :param kwargs_head: Additional attributes to apply to the modal header.
    :param kwargs_body: Additional attributes to apply to the modal body.
    :param kwargs_footer: Additional attributes to apply to the modal footer.
    :param kwargs: Additional attributes to apply to the modal container.
    """
    with _Modal(**kwargs) as modal:
        # Modal card
        with div(_class="modal-card"):

            # Modal header
            with header(
                _class=f"modal-card-head {_class_head}",
                **kwargs_head,
            ):
                p(
                    "",
                    _class="modal-card-title",
                    **{
                        "x-text": "$store.modal.title",
                    }
                )
                button(
                    _class=f"delete",
                    _aria_label="close",
                    **{
                        ":class": "{ 'is-hidden': !$store.modal.closeable }",
                        "@click": "$store.modal.show = false",
                    },
                )

            # Modal body
            section(
                "",
                _class=f"modal-card-body {_class_body}",
                **kwargs_body,
                **{
                    ":class": "{ 'is-hidden': $store.modal.body == '' }",
                    "x-html": "$store.modal.body",
                }
            )

            # Modal footer
            footer(
                "",
                _class=f"modal-card-foot {_class_foot}",
                **kwargs_footer,
                **{
                    "x-html": "$store.modal.footer",
                }
            )
    return modal


def Modal(**kwargs):
    """
    Create a simple modal component.
    """

    with _Modal(**kwargs) as modal:
        # Modal content
        div(_class="modal-content", **{
            "x-html": "$store.modal.body",
        })
    return modal


__all__ = [
    "ModalCard",
    "Modal",
]
