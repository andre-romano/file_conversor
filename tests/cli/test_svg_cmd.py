# tests\cli\test_svg_cmd.py

from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_svg_convert_jpg(tmp_path):
    in_path = DATA_PATH / "test.svg"
    out_path = tmp_path / "test.jpg"

    result = Test.invoke("svg", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_svg_convert_png(tmp_path):
    in_path = DATA_PATH / "test.svg"
    out_path = tmp_path / "test.png"

    result = Test.invoke("svg", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_svg():
    result = Test.invoke("svg", "--help")
    assert "svg" in result.output
