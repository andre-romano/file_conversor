# tests\cli\test_doc_cmd.py


from tests.utils import Test, DATA_PATH


def test_doc_convert_odt(tmp_path):
    in_path = DATA_PATH / "test.docx"
    out_path = tmp_path / "test.odt"

    process = Test.run("doc", "convert", str(in_path), "-o", str(out_path))

    assert process.returncode == 0
    assert out_path.exists()


def test_doc_convert_pdf(tmp_path):
    in_path = DATA_PATH / "test.docx"
    out_path = tmp_path / "test.pdf"

    process = Test.run("doc", "convert", str(in_path), "-o", str(out_path))
    assert process.returncode == 0
    assert out_path.exists()


def test_doc_convert():
    result = Test.invoke("doc", "convert", "--help")
    assert "doc convert" in result.output


def test_doc():
    result = Test.invoke("doc", "--help")
    assert "doc" in result.output
