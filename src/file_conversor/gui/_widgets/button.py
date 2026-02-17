# src/file_conversor/gui/_widgets/button.py

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QToolButton


def _set_icon(button: QPushButton | QToolButton, icon: tuple[Path, int, int] | tuple[QIcon, int, int] | None) -> None:
    match icon:
        case None:
            """do nothing"""
        case (Path() as icon_file, int() as icon_width, int() as icon_height):
            assert icon_file.exists(), f"Icon file not found: {icon_file}"
            button.setIcon(QIcon(str(icon_file)))
            if icon_width > 0 and icon_height > 0:
                button.setIconSize(QSize(icon_width, icon_height))
        case (QIcon() as icon_obj, int() as icon_width, int() as icon_height):
            button.setIcon(icon_obj)
            if icon_width > 0 and icon_height > 0:
                button.setIconSize(QSize(icon_width, icon_height))


class PushButton(QPushButton):
    def __init__(
            self,
            icon: tuple[Path, int, int] | tuple[QIcon, int, int] | None = None,
            tooltip: str = "",
            btn_size: tuple[int, int] | None = None,
            checkable: bool = True,
    ) -> None:
        super().__init__()

        _set_icon(self, icon)
        if btn_size is not None:
            self.setFixedSize(QSize(*btn_size))
        if tooltip:
            self.setToolTip(tooltip)
        self.setCheckable(checkable)


class ToolButton(QToolButton):
    Style = Qt.ToolButtonStyle

    def __init__(
            self,
            icon: tuple[Path, int, int] | tuple[QIcon, int, int] | None = None,
            tooltip: str = "",
            btn_size: tuple[int, int] | None = None,
            checkable: bool = True,
            style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonIconOnly,
    ) -> None:
        super().__init__(autoRaise=True)

        _set_icon(self, icon)
        if btn_size is not None:
            self.setFixedSize(QSize(*btn_size))
        if tooltip:
            self.setToolTip(tooltip)
        self.setCheckable(checkable)
        self.setToolButtonStyle(style)


__all__ = [
    "PushButton",
    "ToolButton",
]
