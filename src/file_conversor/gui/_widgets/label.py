
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(
        self,
        text: str = "",
        stylesheet: str = "",
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        visible: bool = True,
    ) -> None:
        super().__init__(text=text)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        match size:
            case None:
                """do nothing"""
            case (int() as width, int() as height):
                if width > 0:
                    self.setFixedWidth(width)
                if height > 0:
                    self.setFixedHeight(height)
        if line_width > 0:
            self.setLineWidth(line_width)
        self.setVisible(visible)


class LabelUrl(Label):
    def __init__(
        self,
        url: str,
        text: str = "",
        stylesheet: str = "",
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        visible: bool = True,
    ) -> None:
        if not text:
            text = str(url)
        super().__init__(
            text=f'<a href="{url}">{text}</a>',
            stylesheet=stylesheet,
            size=size,
            line_width=line_width,
            visible=visible,
        )
        self.setOpenExternalLinks(True)


class LabelImage(Label):
    def __init__(
        self,
        image_path: Path,
        size: tuple[int, int],
        stylesheet: str = "",
        visible: bool = True,
    ):
        assert image_path.exists(), f"Image file not found: {image_path}"

        super().__init__(
            stylesheet=stylesheet,
            size=size,
            visible=visible,
        )

        self.setPixmap(QPixmap(str(image_path)))
        self.setScaledContents(True)


__all__ = [
    "Label",
    "LabelUrl",
    "LabelImage",
]
