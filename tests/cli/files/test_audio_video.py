
# tests/cli/test_main.py

from tests.utils import Test, DATA_PATH, app_cmd


def test_audio_video_convert(tmp_path):
    test_cases = [
        (DATA_PATH / "test.mp4", tmp_path / "test.mp3"),
    ]

    for in_path, out_path in test_cases:
        result = Test.invoke(
            "audio-video", "convert",
            str(in_path),
            *Test.get_format_params(out_path),
            *Test.get_out_dir_params(out_path),
        )
        assert result.exit_code == 0
        assert out_path.exists()


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


def test_audio_video():
    result = Test.invoke("audio-video", "--help")
    assert "audio-video" in result.output
