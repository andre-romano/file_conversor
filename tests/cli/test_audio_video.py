
# tests/cli/test_main.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_audio_video_convert():
    result = Test.invoke("audio-video", "convert", "--help")
    assert "audio-video convert" in result.output


def test_audio_video_info():
    result = Test.invoke("audio-video", "info", "--help")
    assert "audio-video info" in result.output


def test_audio_video():
    result = Test.invoke("audio-video", "--help")
    assert "audio-video" in result.output
