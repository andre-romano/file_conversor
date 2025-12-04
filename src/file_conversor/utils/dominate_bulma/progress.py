# src/file_conversor/utils/dominate_bulma/progress.py

from file_conversor.utils.dominate_utils import progress


def Progress(
        _max: int | str = 100,
        _class: str = "",
        **kwargs,
):
    """
    Create a progress bar element.

    :param _max: The maximum value of the progress.
    :param _class: Additional CSS classes for the progress bar.
    """
    return progress(_class=f"progress {_class}", _max=str(_max), **kwargs)


__all__ = [
    'Progress',
]
