
from tests.utils import Test, DATA_PATH, app_cmd


def test_text_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.xml", tmp_path / "test.json"),
        (tmp_path / "test.json", tmp_path / "test.xml"),

        (DATA_PATH / "test.toml", tmp_path / "test.yaml"),
        (DATA_PATH / "test.yaml", tmp_path / "test.toml"),

        (DATA_PATH / "test.yaml", tmp_path / "test.ini"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "text", "convert",
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()


def test_text_convert_help():
    Test.invoke_test_help("text", "convert")
