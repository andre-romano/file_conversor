from tests.utils import Test, DATA_PATH, app_cmd


def test_image_resize_scale(tmp_path):
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


def test_image_resize_width(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_resized.png"

    result = Test.invoke(
        "image", "resize",
        str(in_path),
        "-w", "1024",
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image():
    Test.invoke_test_help("image", "resize")
