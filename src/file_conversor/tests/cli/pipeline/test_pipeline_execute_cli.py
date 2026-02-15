
# tests\cli\pipeline\test_pipeline_execute_cmd.py

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, PipelineTyperGroup
from file_conversor.cli.pipeline import PipelineExecuteCLI
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(PipelineExecuteCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineExecuteCLI:
    def test_pipeline_execute_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PIPELINE.value, PipelineTyperGroup.Commands.EXECUTE.value)
