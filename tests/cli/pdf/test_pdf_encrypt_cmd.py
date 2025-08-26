
from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_encrypt_cases(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_encrypted.pdf"

    result = Test.invoke(
        "pdf", "encrypt",
        str(in_path),
        "-op", "1234",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_encrypt_help():
    Test.invoke_test_help("pdf", "encrypt")
