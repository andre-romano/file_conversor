
# tests/cli/audio_video/test_info.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_audio_video_info(tmp_path):
    test_cases = [
        (DATA_PATH / "test.mp4", tmp_path / "test.mp4"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "audio-video", "info",
            str(in_path),
        )
        assert result.exit_code == 0
        assert "h264" in result.stdout


def test_audio_video_info_help():
    Test.invoke_test_help("audio-video", "info")
