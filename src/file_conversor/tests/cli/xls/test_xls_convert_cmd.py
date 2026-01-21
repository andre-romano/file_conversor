# tests\cli\xls\test_xls_convert_cmd.py

import pytest

from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, XlsTyperGroup
from file_conversor.cli.xls import XlsConvertTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(XlsConvertTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestXlsConvert:
    def test_xls_convert_cases(self, tmp_path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.xlsx", tmp_path / "test.pdf"),
            (DATA_PATH / "test.xlsx", tmp_path / "test.ods"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppCommands.XLS.value, XlsTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
        assert process.returncode == 0
        assert out_path.exists()

    def test_xls_convert_help(self,):
        TestTyper.invoke_test_help(AppCommands.XLS.value, XlsTyperGroup.Commands.CONVERT.value)
