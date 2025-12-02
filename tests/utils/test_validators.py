# tests\utils\test_validators.py

import pytest
import typer

from file_conversor.utils.validators import *


class TestUtilsValidators:
    def test_prompt_retry_on_exception(self, monkeypatch):
        inputs = iter(["invalid", "42"])

        def mock_prompt(*args, **kwargs):
            return next(inputs)

        monkeypatch.setattr(typer, "prompt", mock_prompt)

        def check_callback(value):
            ivalue = int(value)
            if ivalue < 0 or ivalue > 100:
                raise ValueError("Value must be between 0 and 100")
            return ivalue

        result = prompt_retry_on_exception(
            text="Enter a number between 0 and 100:",
            type=str,
            check_callback=check_callback,
            retries=2
        )
        assert result == 42

    def test_check_file_size_format(self):
        assert check_file_size_format("0") == "0"
        assert check_file_size_format("0M") == "0M"
        assert check_file_size_format("1K") == "1K"
        assert check_file_size_format("10M") == "10M"
        assert check_file_size_format("5G") == "5G"
        with pytest.raises(typer.BadParameter):
            check_file_size_format("100XY")
        with pytest.raises(typer.BadParameter):
            check_file_size_format("K")

    def test_check_video_resolution(self):
        assert check_video_resolution("1920:1080") == "1920:1080"
        assert check_video_resolution("1280:720") == "1280:720"
        with pytest.raises(typer.BadParameter):
            check_video_resolution("1920")
        with pytest.raises(typer.BadParameter):
            check_video_resolution("1920x1080")
        with pytest.raises(typer.BadParameter):
            check_video_resolution("1920-1080")
        with pytest.raises(typer.BadParameter):
            check_video_resolution("1920:1080:60")

    def test_check_path_exists(self, tmp_path):
        existing_path = tmp_path
        existing_file = tmp_path / "existing_file.txt"
        existing_file.touch()
        non_existing_file = tmp_path / "non_existing_file.txt"

        assert check_path_exists(existing_path, exists=True) == existing_path
        assert check_path_exists(existing_file, exists=True) == existing_file

        with pytest.raises(typer.BadParameter):
            check_path_exists(non_existing_file, exists=True)
        with pytest.raises(typer.BadParameter):
            check_path_exists(existing_file, exists=False)

    def test_check_file_exists(self, tmp_path):
        existing_file = tmp_path / "existing_file.txt"
        existing_file.touch()
        non_existing_file = tmp_path / "non_existing_file.txt"

        assert check_file_exists(existing_file) == existing_file

        with pytest.raises(typer.BadParameter):
            check_file_exists(tmp_path)

        with pytest.raises(typer.BadParameter):
            check_file_exists(non_existing_file)

    def test_check_dir_exists(self, tmp_path):
        existing_dir = tmp_path / "existing_dir"
        existing_dir.mkdir()
        non_existing_dir = tmp_path / "non_existing_dir"

        assert check_dir_exists(existing_dir, mkdir=False) == existing_dir

        with pytest.raises(typer.BadParameter):
            check_dir_exists(non_existing_dir, mkdir=False)

        result_dir = check_dir_exists(non_existing_dir, mkdir=True)
        assert result_dir == non_existing_dir
        assert non_existing_dir.exists() and non_existing_dir.is_dir()

    def test_check_is_bool_or_none(self):
        assert check_is_bool_or_none(None) is None
        assert check_is_bool_or_none(True) == True
        assert check_is_bool_or_none(False) == False
        assert check_is_bool_or_none("true") == True
        assert check_is_bool_or_none("false") == False
        assert check_is_bool_or_none("True") == True
        assert check_is_bool_or_none("False") == False
        with pytest.raises(typer.BadParameter):
            check_is_bool_or_none("yes")
        with pytest.raises(typer.BadParameter):
            check_is_bool_or_none("no")

    def test_check_positive_int(self):
        assert check_positive_integer(10) == 10
        assert check_positive_integer(0, allow_zero=True) == 0
        with pytest.raises(typer.BadParameter):
            check_positive_integer(-5)
        with pytest.raises(typer.BadParameter):
            check_positive_integer(0, allow_zero=False)

    def test_check_file_format(self):
        format_dict = {"txt": "Text File", "md": "Markdown File"}
        assert check_file_format("document.txt", format_dict) == "document.txt"
        assert check_file_format(["file1.md", "file2.txt"], format_dict) == ["file1.md", "file2.txt"]
        assert check_file_format({"file3.txt": 1, "file4.md": 2}, format_dict) == {"file3.txt": 1, "file4.md": 2}
        assert check_file_format({"file5.txt", "file6.md"}, format_dict) == {"file5.txt", "file6.md"}
        with pytest.raises(typer.BadParameter):
            check_file_format("image.jpg", format_dict)
        with pytest.raises(typer.BadParameter):
            check_file_format(["doc.pdf", "notes.txt"], format_dict)

    def test_check_valid_options(self):
        options = ["option1", "option2", "option3"]
        assert check_valid_options("option1", options) == "option1"
        assert check_valid_options("option2", options) == "option2"
        with pytest.raises(typer.BadParameter):
            check_valid_options("option4", options)
        with pytest.raises(typer.BadParameter):
            check_valid_options(["option1", "option5"], options)

    def test_check_ip_format(self):
        assert check_ip_format("192.168.1.1") == "192.168.1.1"
        assert check_ip_format("255.255.255.255") == "255.255.255.255"
        with pytest.raises(typer.BadParameter):
            check_ip_format("256.100.50.25")
        with pytest.raises(typer.BadParameter):
            check_ip_format("192.168.1")
