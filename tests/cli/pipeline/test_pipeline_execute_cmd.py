
from tests.utils import Test, DATA_PATH, app_cmd


def test_pipeline_execute_help():
    Test.invoke_test_help("pipeline", "execute")
