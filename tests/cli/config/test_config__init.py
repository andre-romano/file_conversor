# tests\cli\config\test__init.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_config_help():
    Test.invoke_test_help("config")
