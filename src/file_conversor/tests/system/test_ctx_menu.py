# src/file_conversor/tests/system/test_ctx_menu.py


from file_conversor.system import ContextMenuItem


class TestContextMenuItem:
    def test_context_menu_item_init(self,):
        cmd = ContextMenuItem(
            name="TestCommand",
            description="A test command",
            args=["notepad.exe"],
            icon=None
        )
        assert cmd.name == "TestCommand"
        assert cmd.description == "A test command"
        assert cmd.args == ["notepad.exe"]
        assert cmd.icon is None
