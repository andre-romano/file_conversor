# tests/system/test_win_ctx_menu.py


from pathlib import Path

from file_conversor.system import ContextMenu, ContextMenuItem, WinContextMenu


class TestWinContextMenu:
    def test_singleton(self,):
        menu1 = WinContextMenu.get_instance()
        menu2 = WinContextMenu.get_instance()
        assert menu1 is menu2

    def test_register_callbacks(self,):
        menu = WinContextMenu.get_instance()

        ctx_item_one = ContextMenuItem(
            name="TestCommand",
            description="A test command",
            args=["check"],
            icon=None,
        )
        ctx_item_two = ContextMenuItem(
            name="TestCommand2",
            description="A test command two",
            args=["check", "-f", "docx"],
            keep_terminal_open=True,
        )

        def register(ctx_menu: ContextMenu, icons_path: Path) -> None:
            ctx_item_two.icon = icons_path / "docx.ico"
            ctx_menu.add_extension(".txt", [
                ctx_item_one,
                ctx_item_two,
            ])
        menu.register_callback(register)
        reg_file = menu.get_reg_file()
        for key_name, key in reg_file.items():
            root_key_stem = "FileConversor"
            if key_name.endswith(rf".txt\shell\{root_key_stem}"):
                assert key["MUIVerb"] == menu.MENU_NAME
                assert key["Icon"] == str(menu.ICON_FILE_PATH)

            if key_name.endswith(rf".txt\shell\{root_key_stem}\shell\{ctx_item_one.name}"):
                assert key["MUIVerb"] == ctx_item_one.description
                assert key["Icon"] == ""

            if key_name.endswith(rf".txt\shell\{root_key_stem}\shell\{ctx_item_one.name}\command"):
                assert key["@"].startswith('cmd.exe /c "')
                assert key["@"].endswith(f'{' '.join(f'"{arg}"' for arg in ctx_item_one.args)} "%1""')

            if key_name.endswith(rf".txt\shell\{root_key_stem}\shell\{ctx_item_two.name}"):
                assert key["MUIVerb"] == ctx_item_two.description
                assert key["Icon"] == str(ctx_item_two.icon)

            if key_name.endswith(rf".txt\shell\{root_key_stem}\shell\{ctx_item_two.name}\command"):
                assert key["@"].startswith('cmd.exe /k "')
                assert key["@"].endswith(f'{' '.join(f'"{arg}"' for arg in ctx_item_two.args)} "%1""')
