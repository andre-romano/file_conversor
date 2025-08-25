# tests\cli\test_doc_cmd.py

from tests.utils import Test, DATA_PATH


def test_ppt_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.pptx", tmp_path / "test.pdf"),
        (DATA_PATH / "test.pptx", tmp_path / "test.odp"),
    ]

    for in_path, out_path in test_cases:
        process = Test.run(
            "ppt", "convert", str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
    assert process.returncode == 0
    assert out_path.exists()


def test_ppt_convert():
    result = Test.invoke("ppt", "convert", "--help")
    assert "ppt convert" in result.output


def test_ppt():
    result = Test.invoke("ppt", "--help")
    assert "ppt" in result.output
