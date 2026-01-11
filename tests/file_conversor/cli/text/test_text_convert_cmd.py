# tests\cli\text\test_text_convert_cmd.py

import pytest

from file_conversor.cli.text._typer import COMMAND_NAME, CONVERT_NAME
from file_conversor.cli.text.convert_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextConvert:
    def test_text_convert_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.xml", tmp_path / "test.json"),
            (tmp_path / "test.json", tmp_path / "test.xml"),

            (DATA_PATH / "test.toml", tmp_path / "test.yaml"),
            (DATA_PATH / "test.yaml", tmp_path / "test.toml"),

            (DATA_PATH / "test.yaml", tmp_path / "test.ini"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CONVERT_NAME,
                str(in_path),
                *Test.get_format_params(out_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_text_convert_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
