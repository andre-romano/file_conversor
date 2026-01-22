# tests\cli\test_pipeline_cmd.py

import pytest
from pathlib import Path

# user-provided imports
from file_conversor.cli import AppTyperGroup, PipelineTyperGroup
from file_conversor.cli.pipeline import PipelineCreateTyperCommand

from file_conversor.tests.utils import TestTyper, DATA_PATH


@pytest.mark.skipif(not TestTyper.dependencies_installed(PipelineCreateTyperCommand.EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestPipelineCreate:
    def test_pipeline_create_help(self,):
        TestTyper.invoke_test_help(AppTyperGroup.Commands.PIPELINE.value, PipelineTyperGroup.Commands.CREATE.value)
