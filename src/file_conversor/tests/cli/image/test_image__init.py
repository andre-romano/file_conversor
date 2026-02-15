# tests\file_conversor\cli\image\test_image__init.py


# user-provided modules
from file_conversor.cli import AppTyperGroup, ImageTyperGroup
from file_conversor.tests.utils import TestTyper


class TestImageHelpCLI:
    def test_image_help(self,):
        result = TestTyper.invoke(AppTyperGroup.Commands.IMAGE.value, "--help")
        for mode in ImageTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
