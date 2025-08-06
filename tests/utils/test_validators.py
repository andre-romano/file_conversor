
import pytest
import typer

from file_conversor.utils.validators import *


def test_check_positive_integer_valid():
    assert check_positive_integer(1) == 1
    assert check_positive_integer(10) == 10
    assert check_positive_integer(1000) == 1000


def test_check_positive_integer_invalid_zero():
    with pytest.raises(typer.BadParameter) as excinfo:
        check_positive_integer(0)
    assert "Bitrate must be a positive integer." in str(excinfo.value)


def test_check_positive_integer_invalid_negative():
    with pytest.raises(typer.BadParameter) as excinfo:
        check_positive_integer(-5)
    assert "Bitrate must be a positive integer." in str(excinfo.value)


def test_check_positive_integer_float():
    assert check_positive_integer(5.0) == 5.0


def test_check_format_valid_dict():
    formats = {"mp3": {}, "wav": {}}
    assert check_file_format("mp3", formats) == "mp3"
    assert check_file_format("wav", formats) == "wav"


def test_check_format_valid_list():
    formats = ["mp3", "wav", "flac"]
    assert check_file_format("mp3", formats) == "mp3"
    assert check_file_format("flac", formats) == "flac"


def test_check_format_invalid_dict():
    formats = {"mp3": {}, "wav": {}}
    with pytest.raises(typer.BadParameter) as excinfo:
        check_file_format("aac", formats)
    assert "Unsupported format 'aac'" in str(excinfo.value)
    assert "mp3" in str(excinfo.value)
    assert "wav" in str(excinfo.value)


def test_check_format_invalid_list():
    formats = ["mp3", "wav"]
    with pytest.raises(typer.BadParameter) as excinfo:
        check_file_format("ogg", formats)
    assert "Unsupported format 'ogg'" in str(excinfo.value)
    assert "mp3" in str(excinfo.value)
    assert "wav" in str(excinfo.value)
