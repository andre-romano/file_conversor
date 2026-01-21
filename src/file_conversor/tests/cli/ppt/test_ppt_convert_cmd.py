# tests\cli\ppt\test_ppt_convert_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, PptTyperGroup
from file_conversor.cli.ppt import PptConvertTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PptConvertTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPptConvert:
    def test_ppt_convert_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.pptx", tmp_path / "test.pdf"),
            (DATA_PATH / "test.pptx", tmp_path / "test.odp"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppCommands.PPT.value, PptTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
        assert process.returncode == 0
        assert out_path.exists()

    def test_ppt_convert_help(self,):
        TestTyper.invoke_test_help(AppCommands.PPT.value, PptTyperGroup.Commands.CONVERT.value)
