
# tests/cli/audio_video/test__help.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_audio_video_help():
    Test.invoke_test_help("audio-video")
