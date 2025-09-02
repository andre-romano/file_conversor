# tests\cli\xls\test_xls_convert_cmd.py

import pytest

from file_conversor.cli.xls._typer import COMMAND_NAME, CONVERT_NAME
from file_conversor.cli.xls.convert_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestXlsConvert:
    def test_xls_convert_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.xlsx", tmp_path / "test.pdf"),
            (DATA_PATH / "test.xlsx", tmp_path / "test.ods"),
        ]

        # for in_path, out_path in test_cases:
        #     process = Test.run(
        #         COMMAND_NAME,CONVERT_NAME, str(in_path),
        #         *Test.get_format_params(out_path),
        #         *Test.get_out_dir_params(out_path),
        #     )
        # assert process.returncode == 0
        # assert out_path.exists()

    def test_xls_convert_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CONVERT_NAME)
