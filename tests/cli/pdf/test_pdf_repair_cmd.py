# tests\cli\pdf\test_pdf_repair_cmd.py

from pathlib import Path

from file_conversor.cli.pdf._typer import COMMAND_NAME, REPAIR_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_repair_cases(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_repaired.pdf"

    result = Test.invoke(
        COMMAND_NAME, REPAIR_NAME,
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_repair_help():
    Test.invoke_test_help(COMMAND_NAME, REPAIR_NAME)
