# tests\cli\test_pdf_cmd.py

from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_decrypt(tmp_path):
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

    in_path = out_path
    out_path = tmp_path / "test_encrypted_decrypted.pdf"

    result = Test.invoke(
        "pdf", "decrypt",
        str(in_path),
        "-p", "1234",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_encrypt(tmp_path):
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


def test_pdf_rotate(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_rotated.pdf"

    result = Test.invoke(
        "pdf", "rotate",
        str(in_path),
        "-r", "1-:90",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_extract_img(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke(
        "pdf", "extract-img",
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0


def test_pdf_extract(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_extracted.pdf"

    result = Test.invoke(
        "pdf", "extract",
        str(in_path),
        "-pg", "1-1",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_split(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke(
        "pdf", "split",
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.with_name(f"test_1{out_path.suffix}").exists()


def test_pdf_merge(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_merged.pdf"

    result = Test.invoke(
        "pdf", "merge",
        str(in_path),
        *Test.get_out_file_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_convert(tmp_path):
    test_cases = [
        (DATA_PATH / "test.pdf", tmp_path / "test.jpg"),
        (DATA_PATH / "test.pdf", tmp_path / "test.png"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "pdf", "convert",
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.with_name(f"test_1{out_path.suffix}").exists()


def test_pdf_compress(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_compressed.pdf"

    result = Test.invoke(
        "pdf", "compress",
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_repair(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_repaired.pdf"

    result = Test.invoke(
        "pdf", "repair",
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf():
    result = Test.invoke("pdf", "--help")
    assert "pdf" in result.output
