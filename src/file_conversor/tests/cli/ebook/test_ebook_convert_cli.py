# tests\cli\ebook\test_ebook_convert_cli.py

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, EbookTyperGroup
from file_conversor.cli.ebook import EbookConvertCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(EbookConvertCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestEbookConvertCLI:
    def test_ebook_convert_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.epub", tmp_path / "test.pdf"),
            (DATA_PATH / "test.epub", tmp_path / "test.docx"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppTyperGroup.Commands.EBOOK.value, EbookTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert process.returncode == 0
            assert out_path.exists()

    def test_ebook_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.EBOOK.value, EbookTyperGroup.Commands.CONVERT.value)
