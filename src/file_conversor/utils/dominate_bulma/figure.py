# src\file_conversor\backend\gui\_components\figure.py

from file_conversor.utils.dominate_utils import figure, img


def Figure(
        _src: str,
        _alt: str = '',
        _class="",
        **kwargs,
):
    """
    Create a figure element with an image.

    :param _src: The source URL of the image.
    :param _alt: The alt text for the image.
    :param _class: Additional CSS classes for the figure.
    """
    with figure(_class=f"image {_class}", **kwargs) as fig:
        img(
            src=_src,
            alt=_alt,
        )
    return fig


__all__ = [
    'Figure',
]
