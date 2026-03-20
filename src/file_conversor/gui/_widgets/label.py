
from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QResizeEvent
from PySide6.QtWidgets import QLabel, QSizePolicy


class Label(QLabel):
    AlignmentFlag = Qt.AlignmentFlag

    def __init__(
        self,
        text: str = "",
        name: str = "",
        stylesheet: str = "",
        max_size: tuple[int, int] | None = None,
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        alignment: AlignmentFlag | None = None,
        word_wrap: bool = False,
        visible: bool = True,
    ) -> None:
        super().__init__(text=text)
        self.setObjectName(name)
        self.setStyleSheet(stylesheet) if stylesheet else None
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)  # set the size policy to maximum to prevent expansion
        if max_size:
            self.setMaximumSize(*max_size)  # set the maximum size of the widget
        if size:
            self.setFixedSize(*size)
        self.setLineWidth(line_width) if line_width > 0 else None
        self.setAlignment(alignment) if alignment else None
        self.setWordWrap(word_wrap)
        self.hide() if not visible else None


class LabelUrl(Label):
    def __init__(
        self,
        url: str,
        text: str = "",
        name: str = "",
        stylesheet: str = "",
        max_size: tuple[int, int] | None = None,
        size: tuple[int, int] | None = None,
        line_width: int = 0,
        alignment: Label.AlignmentFlag | None = None,
        word_wrap: bool = False,
        visible: bool = True,
    ) -> None:
        if not text:
            text = str(url)
        super().__init__(
            text=f'<a href="{url}">{text}</a>',
            name=name,
            stylesheet=stylesheet,
            max_size=max_size,
            size=size,
            line_width=line_width,
            alignment=alignment,
            word_wrap=word_wrap,
            visible=visible,
        )
        self.setOpenExternalLinks(True)


class LabelImage(Label):
    def __init__(
        self,
        image: Path | QIcon,
        size: tuple[int, int],
        max_size: tuple[int, int] | None = None,
        name: str = "",
        stylesheet: str = "",
        alignment: Label.AlignmentFlag | None = None,
        visible: bool = True,
    ):
        super().__init__(
            name=name,
            stylesheet=stylesheet,
            max_size=max_size,
            size=size,
            alignment=alignment,
            visible=visible,
        )

        if isinstance(image, Path):
            assert image.exists(), f"Image file not found: {image}"
            icon = QIcon(str(image))
        elif isinstance(image, QIcon):
            icon = image
        pixmap = icon.pixmap(*size)
        self.setPixmap(pixmap)

    @override
    def resizeEvent(self, event: QResizeEvent):
        # scale the pixmap to fit the new size while keeping the aspect ratio
        pixmap = self.pixmap()
        if pixmap.isNull():
            return
        pixmap_scaled = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(pixmap_scaled)

        # call the base class implementation to ensure proper event handling
        super().resizeEvent(event)


__all__ = [
    "Label",
    "LabelUrl",
    "LabelImage",
]
