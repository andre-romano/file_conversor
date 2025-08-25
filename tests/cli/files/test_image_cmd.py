# tests\cli\test_image_cmd.py

from pathlib import Path
from tests.utils import Test, DATA_PATH, app_cmd


def test_image_resize(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_resized.png"

    result = Test.invoke(
        "image", "resize",
        str(in_path),
        "-s", "2.0",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_mirror_x(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_mirrored.png"

    result = Test.invoke(
        "image", "mirror",
        str(in_path),
        "-a", "x",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_rotate(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_rotated.png"

    result = Test.invoke(
        "image", "rotate",
        str(in_path),
        "-r", "90",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_convert_png_jpg(tmp_path):
    test_cases = [
        (DATA_PATH / "test.png", tmp_path / "test.jpg"),
        (tmp_path / "test.jpg", tmp_path / "test.png"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "image", "convert",
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()


def test_image_render(tmp_path):
    test_cases = [
        (DATA_PATH / "test.svg", tmp_path / "test.jpg"),
        (DATA_PATH / "test.svg", tmp_path / "test.png"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "image", "render",
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()


def test_image_to_pdf(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke(
        "image", "to-pdf",
        str(in_path),
        *Test.get_out_file_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_info():
    in_path = DATA_PATH / "test.png"

    result = Test.invoke("image", "info", str(in_path))
    assert result.exit_code == 0
    assert "PNG" in result.stdout


def test_image_compress(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_compressed.png"

    result = Test.invoke(
        "image", "compress",
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image():
    result = Test.invoke("image", "--help")
    assert "image" in result.output
