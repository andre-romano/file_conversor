import stat

from pathlib import Path

from file_conversor.backend.lin_desktop_backend import LinDesktopBackend


class TestLinDesktopBackend:
    def test_install_marks_desktop_file_executable(self, tmp_path: Path):
        backend = LinDesktopBackend()
        desktop_file = tmp_path / "test.desktop"

        backend.install({desktop_file: "[Desktop Entry]\nType=Service\n"})

        file_mode = desktop_file.stat().st_mode
        assert desktop_file.exists()
        assert file_mode & stat.S_IXUSR
