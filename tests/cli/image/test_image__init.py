
from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_image_help():
    Test.invoke_test_help("image")
