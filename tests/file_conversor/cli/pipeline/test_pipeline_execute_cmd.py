
# tests\cli\pipeline\test_pipeline_execute_cmd.py

import pytest

from file_conversor.cli.pipeline._typer import COMMAND_NAME, EXECUTE_NAME
from file_conversor.cli.pipeline.execute_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineExecute:
    def test_pipeline_execute_help(self,):
        Test.invoke_test_help(COMMAND_NAME, EXECUTE_NAME)
