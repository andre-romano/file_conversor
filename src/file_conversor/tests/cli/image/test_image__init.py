# tests\file_conversor\cli\image\test_image__init.py


from pathlib import Path

# user-provided modules
from file_conversor.cli._typer import AppCommands, ImageTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestImageHelp:
    def test_image_help(self,):
        result = TestTyper.invoke(AppCommands.IMAGE.value, "--help")
        for mode in ImageTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
