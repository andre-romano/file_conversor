# tests\cli\text\test_text_check_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, TextTyperGroup
from file_conversor.cli.text import TextCheckTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(TextCheckTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextCheck:
    def test_text_check_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.xml", Path(tmp_path)),
        ]

        for in_path, _ in test_cases:
            result = TestTyper.invoke(
                AppCommands.TEXT.value, TextTyperGroup.Commands.CHECK.value,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_text_check_help(self,):
        TestTyper.invoke_test_help(AppCommands.TEXT.value, TextTyperGroup.Commands.CHECK.value)
