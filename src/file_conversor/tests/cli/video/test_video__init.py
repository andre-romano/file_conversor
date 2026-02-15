
# tests/cli/video/test_av__init.py

# user-provided modules
from file_conversor.cli import AppTyperGroup, VideoTyperGroup
from file_conversor.tests.utils import TestTyper


class TestVideoHelpCLI:
    def test_video_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.VIDEO.value, "--help")
        for mode in VideoTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
