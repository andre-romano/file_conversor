# src\file_conversor\backend\gui\_components\card.py

from typing import Any

from file_conversor.utils.dominate_utils import a, button, div, header, p, footer


def Card(
    content: Any = None,
        top_image: Any = None,
        header_data: dict[str, Any] | None = None,
        footer_data: list[dict[str, Any]] | None = None,
        **kwargs,
):
    """
    Create a card component.

    :param content: The card content data to display in the card.
    :param top_image: The card image content (Figure or img tag).
    :param header_data: The card header content. {"title": str, "icon": FontAwesomeIcon}
    :param footer_data: The card footer content. list[{"text": str, "link": str}]
    """
    with div(_class="card", **kwargs) as card:
        # Card image section
        if top_image:
            with div(_class="card-image") as card_image:
                card_image.add(top_image)

        if header_data:
            with header(_class="card-header"):
                p(header_data["title"], _class="card-header-title")
                button(header_data["icon"], _class="card-header-icon", _aria_label="more options")

        # Card content section
        if content:
            with div(_class="card-content") as card_content:
                card_content.add(content)

        # Card footer section (optional)
        if footer_data:
            with footer(_class="card-footer"):
                for item in footer_data:
                    a(item["text"], _class="card-footer-item", _href=item["link"])
    return card


__all__ = [
    'Card',
]
