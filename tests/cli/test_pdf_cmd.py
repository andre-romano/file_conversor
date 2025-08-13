# tests\cli\test_pdf_cmd.py

from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_pdf_decrypt(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_decrypted.pdf"

    result = Test.invoke("pdf", "decrypt", str(in_path), "-o", str(out_path), "-p", "1234")
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_encrypt(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_encrypted.pdf"

    result = Test.invoke("pdf", "encrypt", str(in_path), "-o", str(out_path), "-op", "1234")
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_rotate(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_rotateed.pdf"

    result = Test.invoke("pdf", "rotate", str(in_path), "-o", str(out_path), "-r", "1:90")
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_extract(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_extracted.pdf"

    result = Test.invoke("pdf", "extract", str(in_path), "-o", str(out_path), "-pg", "1")
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_split(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_splitted.pdf"

    result = Test.invoke("pdf", "split", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert Path(tmp_path) / f"{out_path.name.rstrip(".pdf")}_1.pdf"


def test_pdf_merge(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_merge.pdf"

    result = Test.invoke("pdf", "merge", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_repair(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test_repair.pdf"

    result = Test.invoke("pdf", "repair", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_convert_png(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test.png"

    result = Test.invoke("pdf", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.with_name("test_1.png").exists()


def test_pdf_convert_jpg(tmp_path):
    in_path = DATA_PATH / "test.pdf"
    out_path = tmp_path / "test.jpg"

    result = Test.invoke("pdf", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.with_name("test_1.jpg").exists()


def test_pdf():
    result = Test.invoke("pdf", "--help")
    assert "pdf" in result.output
