# src/file_conversor/gui/_widgets/utils.py

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLayout, QVBoxLayout, QWidget

from file_conversor.config import Log


LOG = Log.get_instance()
logger = LOG.getLogger(__name__)


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


def get_qt_icon(
        name: str,
        prefix: Literal["mdi", "mdi6", "fa5", "fa6", "ei", "ph", "ri", "msc"] = "mdi",
        color: str = 'black',
        color_active: str = 'gray',
) -> QIcon:
    import qtawesome as qta  # pyright: ignore[reportMissingTypeStubs]
    return qta.icon(f"{prefix}.{name}", color=color, color_active=color_active)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


def get_app_icon(icon_path: Path) -> QIcon:
    icon_path = icon_path / "icon.png"
    assert icon_path.exists(), f"'App icon file not found:' {icon_path}"
    return QIcon(str(icon_path))


def get_file_filter(*extensions: str, description: str) -> str:
    ext_str = " ".join(f"*.{ext.lstrip(".").lower()}" for ext in extensions)
    return f"{description} ({ext_str})"


def get_file_extensions(file_filters: str) -> list[str]:
    """ 
    Extract file extensions from a filter string like "Text Files (*.txt);;Images (*.png *.jpg);;All Files (*.*)" 

    :param file_filters: The filter string to parse
    :return: A list of file extensions (e.g. [".txt", ".png", ".jpg", ".*"])
    """
    import re
    extensions: list[str] = []
    for filter in file_filters.split(";;"):
        if not filter:
            continue
        match = re.match(r".+\((\*\..+)\)$", filter.strip())
        if not match:
            continue
        exts = match.group(1).split()
        extensions.extend(f".{re.sub(r"^\**\.*", "", ext).lower()}" for ext in exts)
    logger.debug(f"get_file_extensions() = {extensions}")
    return extensions


def configure_qt_window(
        window: QWidget,
        icon_path: Path,
        title: str = "",
        min_size: tuple[int, int] = (400, 150),
        max_size: tuple[int, int] | None = None,
        size: tuple[int, int] | None = None,
) -> None:
    window.setWindowTitle(f"{title} - File Conversor" if title else "File Conversor")
    window.setWindowIcon(get_app_icon(icon_path))

    window.setMinimumSize(*min_size)
    if max_size:
        window.setMaximumSize(*max_size)
    if size:
        window.resize(*size)


__all__ = [
    "Stretch",
    "get_hlayout",
    "get_vlayout",
    "get_qt_icon",
    "get_app_icon",
    "configure_qt_window",
]
