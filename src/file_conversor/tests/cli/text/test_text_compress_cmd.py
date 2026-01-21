# tests\cli\text\test_text_compress_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, TextTyperGroup
from file_conversor.cli.text import TextCompressTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(TextCompressTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextCompress:
    def test_text_compress_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.xml", tmp_path / "test_compressed.xml"),
            (DATA_PATH / "test.json", tmp_path / "test_compressed.json"),
            (DATA_PATH / "test.yaml", tmp_path / "test_compressed.yaml"),
            (DATA_PATH / "test.toml", tmp_path / "test_compressed.toml"),
            (DATA_PATH / "test.ini", tmp_path / "test_compressed.ini"),
        ]

        for in_path, out_path in test_cases:
            result = TestTyper.invoke(
                AppCommands.TEXT.value, TextTyperGroup.Commands.COMPRESS.value,
                str(in_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert result.exit_code == 0
            assert out_path.exists()

    def test_text_compress_help(self,):
        TestTyper.invoke_test_help(AppCommands.TEXT.value, TextTyperGroup.Commands.COMPRESS.value)
