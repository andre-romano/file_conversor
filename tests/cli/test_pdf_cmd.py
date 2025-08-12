# tests\cli\test_pdf_cmd.py

from pathlib import Path
from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_pdf_decrypt(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_decrypted.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "decrypt", str(in_path), "-o", str(out_path), "-p", "1234"]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_encrypt(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_encrypted.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "encrypt", str(in_path), "-o", str(out_path), "-op", "1234"]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_rotate(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_rotateed.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "rotate", str(in_path), "-o", str(out_path), "-r", "1:90"]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_extract(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_extracted.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "extract", str(in_path), "-o", str(out_path), "-pg", "1"]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_split(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_splitted.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "split", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert Path(tmp_path) / f"{out_path.name.rstrip(".pdf")}_1.pdf"


def test_pdf_merge(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_merge.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "merge", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_repair(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test_repair.pdf"

    result = runner.invoke(
        app_cmd, ["pdf", "repair", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_pdf_convert_png(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test.png"

    result = runner.invoke(
        app_cmd, ["pdf", "convert", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.with_name("test_1.png").exists()


def test_pdf_convert_jpg(tmp_path):
    in_path = Path("tests/.data/test.pdf").resolve()
    out_path = tmp_path / "test.jpg"

    result = runner.invoke(
        app_cmd, ["pdf", "convert", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.with_name("test_1.jpg").exists()


def test_pdf():
    result = runner.invoke(app_cmd, ["pdf", "--help"])
    assert "pdf" in result.output
