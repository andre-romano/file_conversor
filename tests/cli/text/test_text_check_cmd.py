# tests\cli\text\test_text_check_cmd.py

import pytest

from file_conversor.cli.text._typer import COMMAND_NAME, CHECK_NAME
from file_conversor.cli.text.check_cmd import EXTERNAL_DEPENDENCIES

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestTextCheck:
    def test_text_check_cases(self, tmp_path):
        test_cases = [
            (DATA_PATH / "test.xml", tmp_path),
        ]

        for in_path, _ in test_cases:
            result = Test.invoke(
                COMMAND_NAME, CHECK_NAME,
                str(in_path),
            )
            assert result.exit_code == 0

    def test_text_check_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CHECK_NAME)
