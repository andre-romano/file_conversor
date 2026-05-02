from pathlib import Path

from file_conversor.system import ContextMenu, ContextMenuItem
from file_conversor.system.lin.ctx_menu import LinuxContextMenu


class TestLinuxContextMenu:
    def setup_method(self):
        LinuxContextMenu._instance = None

    def test_register_callbacks_groups_by_mime_and_dedupes(self):
        menu = LinuxContextMenu.get_instance()

        ctx_item = ContextMenuItem(
            name="to_png",
            description="To PNG",
            args=["image", "convert", "-f", "png"],
            icon=None,
        )

        def register(ctx_menu: ContextMenu, _icons_path: Path) -> None:
            ctx_menu.add_extension(".jpg", [ctx_item])
            ctx_menu.add_extension(".jpeg", [ctx_item])

        menu.register_callback(register)
        desktop_files = menu.get_desktop_files()

        assert len(desktop_files) == 1
        content = next(iter(desktop_files.values()))
        assert "X-KDE-Submenu=File Conversor" in content
        assert "MimeType=image/jpeg;" in content
        assert content.count("Name=To PNG") == 1
        assert "Exec=" in content
        assert f'{Path(menu._exe_path).parent / Path(menu._exe_path).name}' not in content
        assert f'{Path(__import__("sys").executable)} -m file_conversor image convert -f png %F' in content
