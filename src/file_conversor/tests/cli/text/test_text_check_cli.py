# tests\cli\text\test_text_check_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, TextTyperGroup
from file_conversor.cli.text import TextCheckCLI
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(TextCheckCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextCheckCLI:
    def test_text_check_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.xml", Path(tmp_path)),
        ]

        for in_path, _ in test_cases:
            result = TestTyper.invoke(
                AppTyperGroup.Commands.TEXT.value, TextTyperGroup.Commands.CHECK.value,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_text_check_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.TEXT.value, TextTyperGroup.Commands.CHECK.value)
