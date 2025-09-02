# tests\cli\text\test_text_compress_cmd.py

import pytest

from file_conversor.cli.text._typer import COMMAND_NAME, COMPRESS_NAME
from file_conversor.cli.text.compress_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextCompress:
    def test_text_compress_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.xml", tmp_path / "test_compressed.xml"),
            (DATA_PATH / "test.json", tmp_path / "test_compressed.json"),
            (DATA_PATH / "test.yaml", tmp_path / "test_compressed.yaml"),
            (DATA_PATH / "test.toml", tmp_path / "test_compressed.toml"),
            (DATA_PATH / "test.ini", tmp_path / "test_compressed.ini"),
        ]

        for in_path, out_path in test_cases:
            result = Test.invoke(
                COMMAND_NAME, COMPRESS_NAME,
                str(in_path),
                *Test.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_text_compress_help(self,):
        Test.invoke_test_help(COMMAND_NAME, COMPRESS_NAME)
