
from tests.utils import Test, DATA_PATH, app_cmd


def test_text_check_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.xml", tmp_path),
    ]

    for in_path, _ in test_cases:
        result = Test.invoke(
            "text", "check",
            str(in_path),
        )
        assert result.exit_code == 0


def test_text_check_help():
    Test.invoke_test_help("text", "check")
