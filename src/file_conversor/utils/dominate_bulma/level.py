# src\file_conversor\backend\gui\_components\level.py

from typing import Any

from file_conversor.utils.dominate_utils import div


def Level(
        center: list[Any] | None = None,
        left: list[Any] | None = None,
        right: list[Any] | None = None,
        **kwargs
):
    with div(_class="level", **kwargs) as level:
        if center:
            with div(_class="level-item has-text-centered") as level_item:
                for item in center:
                    level_item.add(item)
        if left:
            with div(_class="level-left"):
                for item in left:
                    with div(_class="level-item") as level_item:
                        level_item.add(item)
        if right:
            with div(_class="level-right"):
                for item in right:
                    with div(_class="level-item") as level_item:
                        level_item.add(item)
    return level


__all__ = [
    'Level',
]
