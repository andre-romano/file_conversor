# tests\cli\text\test_text_convert_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, TextTyperGroup
from file_conversor.cli.text import TextConvertTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(TextConvertTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
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
            result = TestTyper.invoke(
                AppTyperGroup.Commands.TEXT.value, TextTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_text_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.TEXT.value, TextTyperGroup.Commands.CONVERT.value)
