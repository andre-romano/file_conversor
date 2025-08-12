# tests\cli\test_image_cmd.py

from pathlib import Path
from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_image_mirror_x(tmp_path):
    in_path = Path("tests/.data/test.png").resolve()
    out_path = tmp_path / "test_mirror.png"

    result = runner.invoke(
        app_cmd, ["image", "mirror", str(in_path), "-a", "x", "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_rotate(tmp_path):
    in_path = Path("tests/.data/test.png").resolve()
    out_path = tmp_path / "test_rotated.png"

    result = runner.invoke(
        app_cmd, ["image", "rotate", str(in_path), "-r", "90", "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_convert_webp(tmp_path):
    in_path = Path("tests/.data/test.png").resolve()
    out_path = tmp_path / "test.webp"

    result = runner.invoke(
        app_cmd, ["image", "convert", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_to_pdf(tmp_path):
    in_path = Path("tests/.data/test.png").resolve()
    out_path = tmp_path / "test.pdf"

    result = runner.invoke(
        app_cmd, ["image", "to-pdf", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_info():
    in_path = Path("tests/.data/test.png").resolve()

    result = runner.invoke(
        app_cmd, ["image", "info", str(in_path)]
    )
    assert result.exit_code == 0
    assert "PNG" in result.stdout


def test_image():
    result = runner.invoke(app_cmd, ["image", "--help"])
    assert "image" in result.output
