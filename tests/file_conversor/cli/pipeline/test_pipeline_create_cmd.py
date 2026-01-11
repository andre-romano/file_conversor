# tests\cli\test_pipeline_cmd.py

import pytest

from file_conversor.cli.pipeline._typer import COMMAND_NAME, CREATE_NAME
from file_conversor.cli.pipeline.create_cmd import EXTERNAL_DEPENDENCIES

from tests.file_conversor.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineCreate:
    def test_pipeline_create_help(self,):
        Test.invoke_test_help(COMMAND_NAME, CREATE_NAME)
