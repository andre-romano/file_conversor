# tests/system/test_win_ctx_menu.py


from file_conversor.config import Environment
from file_conversor.system.win import WinContextCommand, WinContextMenu


icons_folder = Environment.get_icons_folder()


class TestWinContextCommand:
    def test_wincontextcommand_init(self,):
        cmd = WinContextCommand(
            name="TestCommand",
            description="A test command",
            command="notepad.exe %1",
            icon=None
        )
        assert cmd.name == "TestCommand"
        assert cmd.description == "A test command"
        assert cmd.command == "notepad.exe %1"
        assert cmd.icon is None


class TestWinContextMenu:
    def test_singleton(self,):
        menu1 = WinContextMenu.get_instance(icons_folder)
        menu2 = WinContextMenu.get_instance(icons_folder)
        assert menu1 is menu2

    def test_register_callbacks(self,):
        menu = WinContextMenu.get_instance(icons_folder)

        def register(ctx_menu: WinContextMenu) -> None:
            ctx_menu.add_extension(".txt", [WinContextCommand(
                name="TestCommand",
                description="A test command",
                command="notepad.exe %1",
                icon=None
            )])
        menu.register_callback(register)
        reg_file = menu.get_reg_file()
        for key_name, key in reg_file.items():
            if key_name.endswith(r".txt\shell\FileConversor"):
                assert key["MUIVerb"] == menu.MENU_NAME
                assert key["Icon"] != ""
            if key_name.endswith(r".txt\shell\FileConversor\shell\TestCommand"):
                assert key["MUIVerb"] == "A test command"
                assert key["Icon"] == ""
            if key_name.endswith(r".txt\shell\FileConversor\shell\TestCommand\command"):
                assert key["@"] == "notepad.exe %1"
