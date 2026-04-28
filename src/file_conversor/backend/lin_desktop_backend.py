# src/file_conversor/backend/lin_desktop_backend.py

"""
Provides functionality for installing and removing KDE Dolphin service-menu
``.desktop`` files and for triggering a KDE service-cache rebuild.
"""

import stat
import subprocess

from pathlib import Path
from typing import Any, Callable, Iterable

from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import LOG


logger = LOG.getLogger(__name__)


class LinDesktopBackend(AbstractBackend):
    """Backend for managing KDE Dolphin service-menu ``.desktop`` files."""

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def install(
        self,
        desktop_files: dict[Path, str],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        """Write each ``{path: content}`` entry to disk, creating parent directories as needed."""
        items = list(desktop_files.items())
        total = len(items)
        if not total:
            progress_callback(100.0)
            return
        for i, (path, content) in enumerate(items):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            logger.info(f"Written: {path}")
            progress_callback((i + 1) / total * 100.0)

    def uninstall(
        self,
        paths: Iterable[Path],
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        """Delete each path if it exists."""
        paths_list = list(paths)
        total = len(paths_list)
        if not total:
            progress_callback(100.0)
            return
        for i, path in enumerate(paths_list):
            if path.exists():
                try:
                    path.unlink()
                    logger.info(f"Removed: {path}")
                except PermissionError:
                    logger.warning(f"Skipping (permission denied): {path}")
            progress_callback((i + 1) / total * 100.0)

    def rebuild_cache(
        self,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        """Run ``kbuildsycoca6`` (or ``kbuildsycoca5``) to refresh the KDE service cache."""
        kbuildsycoca: Path | None = None
        for candidate in ("kbuildsycoca6", "kbuildsycoca5"):
            try:
                kbuildsycoca = self.find_in_path(candidate)
                break
            except FileNotFoundError:
                continue

        if kbuildsycoca is None:
            logger.warning("kbuildsycoca6/kbuildsycoca5 not found in PATH; KDE cache not rebuilt.")
            progress_callback(100.0)
            return

        subprocess.run([str(kbuildsycoca), "--noincremental"], check=True)  # noqa: S603
        progress_callback(100.0)


__all__ = [
    "LinDesktopBackend",
]
