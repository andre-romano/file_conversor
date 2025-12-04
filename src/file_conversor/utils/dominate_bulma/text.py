# src/file_conversor/backend/gui/_components/text.py

from file_conversor.utils.dominate_utils import div, p


def Title(text: str, **kwargs):
    """
    Create a title element.

    :param text: The title text.
    """
    return p(text, _class="title", **kwargs)


def Content(**kwargs):
    """
    Create a content div.
    """
    return div(_class="content", **kwargs)


__all__ = [
    'Content',
]
