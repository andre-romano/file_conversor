# tests\cli\doc\test_convert_cmd.py


from tests.utils import Test, DATA_PATH


def test_doc_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.docx", tmp_path / "test.pdf"),
        (DATA_PATH / "test.docx", tmp_path / "test.odt"),
    ]

    # for in_path, out_path in test_cases:
    #     process = Test.run(
    #         "doc", "convert", str(in_path),
    #         *Test.get_format_params(out_path),
    #         *Test.get_out_dir_params(out_path),
    #     )
    # assert process.returncode == 0
    # assert out_path.exists()


def test_doc_convert_help():
    Test.invoke_test_help("doc", "convert")
