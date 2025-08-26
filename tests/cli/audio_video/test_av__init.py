
# tests/cli/audio_video/test__help.py

from file_conversor.cli.audio_video._typer import COMMAND_NAME

from tests.utils import Test, DATA_PATH, app_cmd


def test_audio_video_help():
    Test.invoke_test_help(COMMAND_NAME)
