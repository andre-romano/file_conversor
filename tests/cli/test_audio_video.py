
# tests/cli/test_main.py

from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd

runner = CliRunner()


def test_audio_video_convert():
    result = runner.invoke(
        app_cmd, ["audio-video", "convert", "--help"])
    assert "audio-video convert" in result.output


def test_audio_video_info():
    result = runner.invoke(
        app_cmd, ["audio-video", "info", "--help"])
    assert "audio-video info" in result.output


def test_audio_video():
    result = runner.invoke(
        app_cmd, ["audio-video", "--help"])
    assert "audio-video" in result.output
