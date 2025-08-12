# tests\cli\test_svg_cmd.py

from pathlib import Path
from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_svg_convert_jpg(tmp_path):
    in_path = Path("tests/.data/test.svg").resolve()
    out_path = tmp_path / "test.jpg"

    result = runner.invoke(
        app_cmd, ["svg", "convert", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_svg_convert_png(tmp_path):
    in_path = Path("tests/.data/test.svg").resolve()
    out_path = tmp_path / "test.png"

    result = runner.invoke(
        app_cmd, ["svg", "convert", str(in_path), "-o", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_svg():
    result = runner.invoke(app_cmd, ["svg", "--help"])
    assert "svg" in result.output
