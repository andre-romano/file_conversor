# tests\cli\image\test_image_convert_cmd.py

from file_conversor.cli.image._typer import COMMAND_NAME, CONVERT_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_image_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.png", tmp_path / "test.jpg"),
        (tmp_path / "test.jpg", tmp_path / "test.png"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            COMMAND_NAME, CONVERT_NAME,
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()


def test_image_convert_help():
    Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
