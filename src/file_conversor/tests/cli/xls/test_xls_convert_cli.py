# tests\cli\xls\test_xls_convert_cmd.py

from pathlib import Path

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, XlsTyperGroup
from file_conversor.cli.xls.convert_cli import XlsConvertCommand
from file_conversor.tests.utils import DATA_PATH, TestTyper


@pytest.mark.skipif(not XlsConvertCommand.check_dependencies(), reason="External dependencies not installed")
class TestXlsConvertCLI:
    def test_xls_convert_cases(self, tmp_path: Path):
        test_cases: list[tuple[Path, Path]] = [
            (DATA_PATH / "test.xlsx", tmp_path / "test.pdf"),
            (DATA_PATH / "test.xlsx", tmp_path / "test.ods"),
        ]

        for in_path, out_path in test_cases:
            process = TestTyper.run(
                AppTyperGroup.Commands.XLS.value, XlsTyperGroup.Commands.CONVERT.value,
                str(in_path),
                *TestTyper.get_format_params(out_path),
                *TestTyper.get_out_dir_params(out_path),
            )
            assert process.returncode == 0
            assert out_path.exists()

    def test_xls_convert_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.XLS.value, XlsTyperGroup.Commands.CONVERT.value)
