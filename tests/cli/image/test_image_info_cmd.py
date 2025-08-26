from tests.utils import Test, DATA_PATH, app_cmd


def test_image_info_cases():
    in_path = DATA_PATH / "test.png"

    result = Test.invoke("image", "info", str(in_path))
    assert result.exit_code == 0
    assert "PNG" in result.stdout


def test_image_info_help():
    Test.invoke_test_help("image", "info")
