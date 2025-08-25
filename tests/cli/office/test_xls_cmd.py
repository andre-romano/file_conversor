# tests\cli\test_xls_cmd.py

from tests.utils import Test, DATA_PATH


def test_xls_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.xlsx", tmp_path / "test.pdf"),
        (DATA_PATH / "test.xlsx", tmp_path / "test.ods"),
    ]

    for in_path, out_path in test_cases:
        process = Test.run(
            "xls", "convert", str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
    assert process.returncode == 0
    assert out_path.exists()


def test_xls_convert():
    result = Test.invoke("xls", "convert", "--help")
    assert "xls convert" in result.output


def test_xls():
    result = Test.invoke("xls", "--help")
    assert "xls" in result.output
