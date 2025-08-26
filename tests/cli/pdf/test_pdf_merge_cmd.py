# tests\cli\pdf\test_pdf_merge_cmd.py

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, MERGE_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_merge_cases(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_merged.pdf"

    result = Test.invoke(
        COMMAND_NAME, MERGE_NAME,
        str(in_path),
        *Test.get_out_file_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf():
    Test.invoke_test_help(COMMAND_NAME, MERGE_NAME)
