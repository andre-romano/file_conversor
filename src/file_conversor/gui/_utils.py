# src/file_conversor/gui/_widgets/utils.py

from dataclasses import dataclass

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLayout, QVBoxLayout, QWidget


@dataclass
class Stretch:
    stretch: int = 1  # noqa: S1700


def get_layout(
    *items: QWidget | QLayout | Stretch,
    layout: QHBoxLayout | QVBoxLayout,
    spacing: int | None = None,
):
    for item in items:
        match item:
            case QWidget():
                layout.addWidget(item)
            case QLayout():
                layout.addLayout(item)
            case Stretch():
                layout.addStretch(item.stretch)
    layout.setSpacing(spacing) if spacing is not None else None
    return layout


def get_hlayout(*items: QWidget | QLayout | Stretch, spacing: int | None = None):
    return get_layout(*items, layout=QHBoxLayout(), spacing=spacing)


def get_vlayout(*items: QWidget | QLayout | Stretch, spacing: int | None = None):
    return get_layout(*items, layout=QVBoxLayout(), spacing=spacing)


def get_qt_icon(name: str, color: str = 'black', color_active: str = 'gray') -> QIcon:
    import qtawesome as qta  # pyright: ignore[reportMissingTypeStubs]
    return qta.icon(name, color=color, color_active=color_active)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


__all__ = [
    "Stretch",
    "get_hlayout",
    "get_vlayout",
    "get_qt_icon",
]
