
# tests\cli\pipeline\test_pipeline__init.py

# user-provided modules
from file_conversor.cli import AppTyperGroup, PipelineTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestPipelineHelp:
    def test_pipeline_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.PIPELINE.value, "--help")
        for mode in PipelineTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
