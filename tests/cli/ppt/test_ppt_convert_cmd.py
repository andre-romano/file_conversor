# tests\cli\ppt\test_ppt_convert_cmd.py

from file_conversor.cli.ppt._typer import COMMAND_NAME, CONVERT_NAME

from tests.utils import Test, DATA_PATH


def test_ppt_convert_cases(tmp_path):
    test_cases = [
        (DATA_PATH / "test.pptx", tmp_path / "test.pdf"),
        (DATA_PATH / "test.pptx", tmp_path / "test.odp"),
    ]

    # for in_path, out_path in test_cases:
    #     process = Test.run(
    #         COMMAND_NAME,CONVERT_NAME, str(in_path),
    #         *Test.get_format_params(out_path),
    #         *Test.get_out_dir_params(out_path),
    #     )
    # assert process.returncode == 0
    # assert out_path.exists()


def test_ppt_convert_help():
    Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
