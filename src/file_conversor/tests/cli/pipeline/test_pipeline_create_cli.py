# tests\cli\test_pipeline_cmd.py

import pytest

# user-provided imports
from file_conversor.cli import AppTyperGroup, PipelineTyperGroup
from file_conversor.cli.pipeline import PipelineCreateCLI
from file_conversor.tests.utils import TestTyper


@pytest.mark.skipif(not TestTyper.dependencies_installed(PipelineCreateCLI.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineCreateCLI:
    def test_pipeline_create_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PIPELINE.value, PipelineTyperGroup.Commands.CREATE.value)
