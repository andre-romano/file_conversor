
from tests.utils import Test, DATA_PATH, app_cmd


def test_text_help():
    Test.invoke_test_help("text")
