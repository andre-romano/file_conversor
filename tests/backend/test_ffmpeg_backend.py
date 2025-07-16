# tests/utils/test_ffmpeg_backend.py

import pytest
import os
import tempfile
import shutil

from backend.ffmpeg_backend import FFmpegBackend


class DummyFile:
    """A dummy file class to mock File behavior for testing."""

    def __init__(self, path):
        super().__init__()
        self.path = path

    def check_supported_format(self, formats):
        ext = self.get_extension()
        if ext not in formats:
            raise ValueError("Unsupported format")

    def get_extension(self):
        return os.path.splitext(self.path)[1][1:].lower()


@pytest.fixture
def dummy_audio_file(tmp_path):
    # Create a dummy file to act as input
    file_path = tmp_path / "test.mp3"
    file_path.write_bytes(b"\x00\x00\x00\x00")
    return str(file_path)


@pytest.fixture
def dummy_output_file(tmp_path):
    return str(tmp_path / "output.wav")


def test_supported_input_formats(tmp_path):
    output_file = tmp_path / "output.mp3"
    output_file.write_bytes(b"dummy")
    for ext in FFmpegBackend.SUPPORTED_IN_FORMATS:
        input_file = tmp_path / f"input.{ext}"
        input_file.write_bytes(b"dummy")
        backend = FFmpegBackend(str(input_file), str(output_file))
        assert isinstance(backend, FFmpegBackend)


def test_supported_output_formats(tmp_path):
    input_file = tmp_path / "input.mp3"
    input_file.write_bytes(b"dummy")
    for ext in FFmpegBackend.SUPPORTED_OUT_FORMATS:
        output_file = tmp_path / f"output.{ext}"
        output_file.write_bytes(b"dummy")
        backend = FFmpegBackend(str(input_file), str(output_file))
        assert isinstance(backend, FFmpegBackend)


def test_set_input_unsupported_format(tmp_path):
    file_path = tmp_path / "test.unsupported"
    file_path.write_bytes(b"dummy")
    backend = FFmpegBackend.__new__(FFmpegBackend)
    with pytest.raises(ValueError):
        backend._set_input(str(file_path))


def test_set_output_unsupported_format(tmp_path):
    file_path = tmp_path / "test.unsupported"
    file_path.write_bytes(b"dummy")
    backend = FFmpegBackend.__new__(FFmpegBackend)
    with pytest.raises(ValueError):
        backend._set_output(str(file_path))


def test_execute_calls_ffmpeg(monkeypatch, tmp_path):
    # Patch ffmpeg.input().output().run() to simulate ffmpeg execution
    class DummyOutput:
        def output(self, *args, **kwargs):
            return self

        def run(self, **kwargs):
            return (b"stdout", b"stderr")

    monkeypatch.setattr("ffmpeg.input", lambda *a, **k: DummyOutput())

    input_file = tmp_path / "input.mp3"
    input_file.write_bytes(b"dummy")
    output_file = tmp_path / "output.mp3"

    backend = FFmpegBackend(str(input_file), str(output_file))
    backend.options = {}
    stdout, stderr = backend.execute()
    assert "stdout" in stdout
    assert "stderr" in stderr


def test_execute_raises_on_ffmpeg_error(monkeypatch, tmp_path):
    class DummyOutput:
        def output(self, *args, **kwargs):
            return self

        def run(self, **kwargs):
            return (b"", b"error: something went wrong")

    monkeypatch.setattr("ffmpeg.input", lambda *a, **k: DummyOutput())

    input_file = tmp_path / "input.mp3"
    input_file.write_bytes(b"dummy")
    output_file = tmp_path / "output.mp3"

    backend = FFmpegBackend(str(input_file), str(output_file))
    backend.options = {}
    with pytest.raises(RuntimeError):
        backend.execute()
