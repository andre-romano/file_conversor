# src/file_conversor/gui/_widgets/button.py

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractButton, QPushButton, QToolButton


def _set_icon(button: QAbstractButton, icon_tuple: tuple[Path, int, int] | tuple[QIcon, int, int]) -> None:
    icon, width, height = icon_tuple
    if isinstance(icon, Path):
        assert icon.exists(), f"Icon file not found: {icon}"
        icon = QIcon(str(icon))
    button.setIcon(icon)
    if width > 0 and height > 0:
        button.setIconSize(QSize(width, height))


class PushButton(QPushButton):
    def __init__(
            self,
            icon: tuple[Path, int, int] | tuple[QIcon, int, int] | None = None,
            tooltip: str = "",
            btn_size: tuple[int, int] | None = None,
            stylesheet: str = "",
            checkable: bool = True,
    ) -> None:
        super().__init__()

        if icon is not None:
            _set_icon(self, icon)
        if btn_size is not None:
            self.setFixedSize(QSize(*btn_size))
        if tooltip:
            self.setToolTip(tooltip)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        self.setCheckable(checkable)


class ToolButton(QToolButton):
    Style = Qt.ToolButtonStyle

    def __init__(
            self,
            icon: tuple[Path, int, int] | tuple[QIcon, int, int] | None = None,
            tooltip: str = "",
            btn_size: tuple[int, int] | None = None,
            stylesheet: str = "",
            checkable: bool = True,
            style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonIconOnly,
    ) -> None:
        super().__init__(autoRaise=True)

        if icon is not None:
            _set_icon(self, icon)
        if btn_size is not None:
            self.setFixedSize(QSize(*btn_size))
        if tooltip:
            self.setToolTip(tooltip)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        self.setCheckable(checkable)
        self.setToolButtonStyle(style)


__all__ = [
    "PushButton",
    "ToolButton",
]
