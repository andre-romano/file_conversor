# tests\cli\test_doc_cmd.py

from tests.utils import Test, DATA_PATH


def test_ppt_convert_odt(tmp_path):
    in_path = DATA_PATH / "test.pptx"
    out_path = tmp_path / "test.odp"
    process = Test.run("ppt", "convert", str(in_path), "-o", str(out_path))
    assert process.returncode == 0
    assert out_path.exists()


def test_ppt_convert_pdf(tmp_path):
    in_path = DATA_PATH / "test.pptx"
    out_path = tmp_path / "test.pdf"

    process = Test.run("ppt", "convert", str(in_path), "-o", str(out_path))
    assert process.returncode == 0
    assert out_path.exists()


def test_ppt_convert():
    result = Test.invoke("ppt", "convert", "--help")
    assert "ppt convert" in result.output


def test_ppt():
    result = Test.invoke("ppt", "--help")
    assert "ppt" in result.output
