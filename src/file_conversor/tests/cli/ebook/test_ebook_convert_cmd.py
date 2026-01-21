# tests\cli\ebook\test_convert_cmd.py

import pytest
from pathlib import Path

from file_conversor.cli._typer import AppCommands, EbookTyperGroup
from file_conversor.cli.ebook import EbookConvertCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(EbookConvertCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestEbookConvert:
    def test_ebook_convert_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.epub", tmp_path / "test.pdf"),
            (DATA_PATH / "test.epub", tmp_path / "test.docx"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppCommands.EBOOK.value, EbookTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
        assert process.returncode == 0
        assert out_path.exists()

    def test_ebook_convert_help(self,):
        TestTyper.invoke_test_help(AppCommands.EBOOK.value, EbookTyperGroup.Commands.CONVERT.value)
