# src\file_conversor\backend\gui\_components\media.py

from typing import Any

from file_conversor.utils.dominate_utils import div


def Media(
        content: Any | None = None,
        left: Any = None,
        right: Any = None,
        **kwargs
):
    with div(_class="media", **kwargs) as media:
        if left:
            with div(_class="media-left") as media_left:
                media_left.add(left)
        if right:
            with div(_class="media-right") as media_right:
                media_right.add(right)
        if content:
            with div(_class="media-content") as media_content:
                media_content.add(content)
    return media


__all__ = [
    'Media',
]
