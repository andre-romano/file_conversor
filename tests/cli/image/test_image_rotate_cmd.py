from tests.utils import Test, DATA_PATH, app_cmd


def test_image_rotate_cases(tmp_path):
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


def test_image_rotate_help():
    Test.invoke_test_help("image", "rotate")
