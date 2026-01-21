
# tests/cli/audio/test_audio__init.py

from file_conversor.cli._typer import AppCommands, AudioTyperGroup

from file_conversor.tests.utils import TestTyper, DATA_PATH


class TestAudioHelp:
    def test_audio_help(self,):
        result = TestTyper.invoke(AppCommands.AUDIO.value, "--help")
        for mode in AudioTyperGroup.Commands:
            assert mode.value in result.output
        assert result.exit_code == 0
