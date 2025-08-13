# tests\cli\test_win_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_win_uninstall_menu():
    result = Test.invoke("win", "uninstall-menu", "--help")
    assert "win uninstall-menu" in result.output


def test_win_install_menu():
    result = Test.invoke("win", "install-menu", "--help")
    assert "win install-menu" in result.output


def test_win():
    result = Test.invoke("win", "--help")
    assert "win" in result.output
