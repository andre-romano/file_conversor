# tests\cli\pdf\test_pdf_extract_img_cmd.py

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, EXTRACT_IMG_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_extract_img_cases(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke(
        COMMAND_NAME, EXTRACT_IMG_NAME,
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0


def test_pdf_extract_img_help():
    Test.invoke_test_help(COMMAND_NAME, EXTRACT_IMG_NAME)
