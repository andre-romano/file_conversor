
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QLabel


class Label(QLabel):
    def __init__(
        self,
        text: str = "",
        stylesheet: str = "",
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        word_wrap: bool = False,
        visible: bool = True,
    ) -> None:
        super().__init__(text=text)
        self.setStyleSheet(stylesheet) if stylesheet else None
        match size:
            case None:
                """do nothing"""
            case (width, height):
                self.setFixedWidth(width) if width > 0 else None
                self.setFixedHeight(height) if height > 0 else None
        self.setLineWidth(line_width) if line_width > 0 else None
        self.setWordWrap(word_wrap)
        self.hide() if not visible else None


class LabelUrl(Label):
    def __init__(
        self,
        url: str,
        text: str = "",
        stylesheet: str = "",
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        word_wrap: bool = False,
        visible: bool = True,
    ) -> None:
        if not text:
            text = str(url)
        super().__init__(
            text=f'<a href="{url}">{text}</a>',
            stylesheet=stylesheet,
            size=size,
            line_width=line_width,
            word_wrap=word_wrap,
            visible=visible,
        )
        self.setOpenExternalLinks(True)


class LabelImage(Label):
    def __init__(
        self,
        image: Path | QIcon,
        size: tuple[int, int],
        stylesheet: str = "",
        visible: bool = True,
    ):
        super().__init__(
            stylesheet=stylesheet,
            size=size,
            visible=visible,
        )

        match image:
            case QIcon():
                pixmap = image.pixmap(*size)
            case Path():
                assert image.exists(), f"Image file not found: {image}"
                pixmap = QPixmap(str(image))
        self.setPixmap(pixmap)
        self.setScaledContents(True)


__all__ = [
    "Label",
    "LabelUrl",
    "LabelImage",
]
