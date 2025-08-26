# tests\cli\pdf\test_pdf_convert_cmd.py

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, CONVERT_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.pdf", tmp_path / "test.jpg"),
        (DATA_PATH / "test.pdf", tmp_path / "test.png"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            COMMAND_NAME, CONVERT_NAME,
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.with_name(f"test_1{out_path.suffix}").exists()


def test_pdf_convert_help():
    Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
