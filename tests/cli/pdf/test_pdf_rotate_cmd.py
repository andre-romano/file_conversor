
# tests\cli\pdf\test_pdf_rotate_cmd.py

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, ROTATE_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_rotate_cases(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_rotated.pdf"

    result = Test.invoke(
        COMMAND_NAME, ROTATE_NAME,
        str(in_path),
        "-r", "1-:90",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_rotate_help():
    Test.invoke_test_help(COMMAND_NAME, ROTATE_NAME)
