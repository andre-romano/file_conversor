
# tests\cli\pipeline\test_pipeline_execute_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli._typer import AppCommands, PipelineTyperGroup
from file_conversor.cli.pipeline import PipelineExecuteTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PipelineExecuteTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineExecute:
    def test_pipeline_execute_help(self,):
        TestTyper.invoke_test_help(AppCommands.PIPELINE.value, PipelineTyperGroup.Commands.EXECUTE.value)
