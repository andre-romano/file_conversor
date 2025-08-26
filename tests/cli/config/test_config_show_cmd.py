# tests\cli\config\test_show_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_show_help():
    Test.invoke_test_help("config", "show")
