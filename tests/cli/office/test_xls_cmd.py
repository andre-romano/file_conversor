# tests\cli\test_xls_cmd.py

from tests.utils import Test, DATA_PATH


def test_xls_convert_odt(tmp_path):
    in_path = DATA_PATH / "test.xlsx"
    out_path = tmp_path / "test.ods"
    process = Test.run("xls", "convert", str(in_path), "-o", str(out_path))
    assert process.returncode == 0
    assert out_path.exists()


def test_xls_convert_pdf(tmp_path):
    in_path = DATA_PATH / "test.xlsx"
    out_path = tmp_path / "test.pdf"

    process = Test.run("xls", "convert", str(in_path), "-o", str(out_path))
    assert process.returncode == 0
    assert out_path.exists()


def test_xls_convert():
    result = Test.invoke("xls", "convert", "--help")
    assert "xls convert" in result.output


def test_xls():
    result = Test.invoke("xls", "--help")
    assert "xls" in result.output
