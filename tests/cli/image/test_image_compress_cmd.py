# tests\cli\image\test_image_compress_cmd.py

from file_conversor.cli.image._typer import COMMAND_NAME, COMPRESS_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_image_compress_cases(tmp_path):
    in_path = DATA_PATH / "test.png"
    out_path = tmp_path / "test_compressed.png"

    result = Test.invoke(
        COMMAND_NAME, COMPRESS_NAME,
        str(in_path),
        *Test.get_out_dir_params(out_path),
    )
    assert result.exit_code == 0
    assert out_path.exists()


def test_image_compress_help():
    Test.invoke_test_help(COMMAND_NAME, COMPRESS_NAME)
