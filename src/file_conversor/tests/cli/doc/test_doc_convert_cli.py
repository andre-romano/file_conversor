# tests\cli\doc\test_convert_cmd.py

from pathlib import Path

import pytest

from file_conversor.cli import AppTyperGroup, DocTyperGroup
from file_conversor.cli.doc import DocConvertCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(DocConvertCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestDocConvertCLI:
    def test_doc_convert_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.docx", tmp_path / "test.pdf"),
            (DATA_PATH / "test.docx", tmp_path / "test.odt"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppTyperGroup.Commands.DOC.value, DocTyperGroup.Commands.CONVERT.value, str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert process.returncode == 0
            assert out_path.exists()

    def test_doc_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.DOC.value, DocTyperGroup.Commands.CONVERT.value)
