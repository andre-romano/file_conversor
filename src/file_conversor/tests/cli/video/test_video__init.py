
# tests/cli/video/test_av__init.py

# user-provided modules
from file_conversor.cli._typer import AppCommands, VideoTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH, app_cmd


class TestVideoHelp:
    def test_video_help(self,):
        result = TestTyper.invoke(AppCommands.VIDEO.value, "--help")
        for mode in VideoTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
