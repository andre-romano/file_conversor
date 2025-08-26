# tests\cli\config\test_set_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_set_help():
    Test.invoke_test_help("config", "set")
