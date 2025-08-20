# tests\cli\test_image_cmd.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_render_svg_jpg(tmp_path):
    in_path = DATA_PATH / "test.svg"
    out_path = tmp_path / "test.jpg"

    result = Test.invoke("image", "render", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_render_svg_png(tmp_path):
    in_path = DATA_PATH / "test.svg"
    out_path = tmp_path / "test.png"

    result = Test.invoke("image", "render", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_mirror_x(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_mirror.png"

    result = Test.invoke("image", "mirror", str(in_path), "-a", "x", "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_rotate(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_rotated.png"

    result = Test.invoke("image", "rotate", str(in_path), "-r", "90", "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_convert_png_jpg(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test.jpg"

    result = Test.invoke("image", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()

    in_path = out_path
    out_path = tmp_path / "test.png"

    result = Test.invoke("image", "convert", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_to_pdf(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke("image", "to-pdf", str(in_path), "-o", str(out_path))
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_info():
    in_path = DATA_PATH / "test.png"

    result = Test.invoke("image", "info", str(in_path))
    assert result.exit_code == 0
    assert "PNG" in result.stdout


def test_image():
    result = Test.invoke("image", "--help")
    assert "image" in result.output
