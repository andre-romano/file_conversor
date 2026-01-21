
# tests\cli\pipeline\test_pipeline__init.py

# user-provided modules
from file_conversor.cli._typer import AppCommands, PipelineTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestPipelineHelp:
    def test_pipeline_help(self,):
        result = TestTyper.invoke(AppCommands.PIPELINE.value, "--help")
        for mode in PipelineTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
