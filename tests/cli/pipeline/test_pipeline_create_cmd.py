# tests\cli\test_pipeline_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_pipeline_create_help():
    Test.invoke_test_help("pipeline", "create")
