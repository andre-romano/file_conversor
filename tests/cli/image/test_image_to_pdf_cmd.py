from tests.utils import Test, DATA_PATH, app_cmd


def test_image_to_pdf_cases(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test.pdf"

    result = Test.invoke(
        "image", "to-pdf",
        str(in_path),
        *Test.get_out_file_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_to_pdf_help():
    Test.invoke_test_help("image", "to-pdf")
