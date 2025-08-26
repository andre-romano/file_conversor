from tests.utils import Test, DATA_PATH, app_cmd


def test_image_render_cases(tmp_path):
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


def test_image_render_help():
    Test.invoke_test_help("image", "render")
