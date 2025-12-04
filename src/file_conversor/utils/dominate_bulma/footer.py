# src\file_conversor\backend\gui\_components\footer.py

from file_conversor.utils.dominate_utils import a, div, span, strong


def Footer(**kwargs):
    """
    Create a footer component with project and license information.
    """
    with div(_id="footer", _class="content has-text-centered", **kwargs) as footer:
        # First line
        with div():
            with strong():
                a(
                    "File Conversor",
                    _href="https://github.com/andre-romano/file_conversor",
                    _target="_blank"
                )
            span(" by ")
            a("Andre Madureira", _href="https://github.com/andre-romano", _target="_blank")

        # Second line (license info)
        with div():
            span("The source code is licensed under the ")
            a(
                "Apache-2.0",
                _href="https://github.com/andre-romano/file_conversor/blob/master/LICENSE",
                _target="_blank"
            )
            span(" license.")
    return footer


__all__ = ["Footer"]
