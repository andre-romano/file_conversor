
# tests/utils/test_file.py

import os
import pytest


from utils.file import File


def test_init_with_invalid_path():
    with pytest.raises(ValueError):
        File(None)  # type: ignore
    with pytest.raises(ValueError):
        File(123)  # type: ignore
    with pytest.raises(ValueError):
        File("")


def test_is_file_and_is_dir(tmp_path):
    # Create a file and a directory
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")

    dir_path = tmp_path / "subdir"
    dir_path.mkdir()

    f_nonexistent = File(str(tmp_path / "nope"))
    f_file = File(str(file_path))
    f_dir = File(str(dir_path))

    assert f_file.is_file() is True
    assert f_file.is_dir() is False

    assert f_dir.is_file() is False
    assert f_dir.is_dir() is True

    assert f_nonexistent.is_file() is False
    assert f_nonexistent.is_dir() is False


def test_create_dir_creates_directory(tmp_path):
    new_dir = tmp_path / "newdir"
    f = File(str(new_dir))
    assert not new_dir.exists()
    f.create_dir()
    assert new_dir.exists()
    assert new_dir.is_dir()


def test_create_dir_raises_if_path_is_file(tmp_path):
    file_path = tmp_path / "afile.txt"
    file_path.write_text("abc")
    f = File(str(file_path))
    with pytest.raises(FileExistsError):
        f.create_dir()


def test_create_dir_existing_dir(tmp_path):
    dir_path = tmp_path / "adir"
    dir_path.mkdir()
    f = File(str(dir_path))
    # Should not raise
    f.create_dir()
    assert dir_path.exists()


def test_check_supported_format_accepts_supported(tmp_path):
    file_path = tmp_path / "test.csv"
    file_path.write_text("abc")
    f = File(str(file_path))
    # Should not raise
    f.check_supported_format(["csv", "txt"])


def test_check_supported_format_raises_for_unsupported(tmp_path):
    file_path = tmp_path / "test.unsupported"
    file_path.write_text("abc")
    f = File(str(file_path))
    with pytest.raises(ValueError) as excinfo:
        f.check_supported_format(["csv", "txt"])
    assert "Unsupported format" in str(excinfo.value)


def test_check_supported_format_with_no_extension(tmp_path):
    file_path = tmp_path / "filewithoutext"
    file_path.write_text("abc")
    f = File(str(file_path))
    with pytest.raises(ValueError):
        f.check_supported_format(["csv", "txt"])


def test_get_dirname_returns_empty_for_no_dir():
    f = File("filename.txt")
    # get_dirname should return '' if no directory part
    assert f.get_dirname() == ""


def test_get_filename_with_multiple_dots(tmp_path):
    file_path = tmp_path / "archive.tar.gz"
    file_path.write_text("abc")
    f = File(str(file_path))
    assert f.get_filename() == "archive.tar"


def test_get_full_path_is_absolute(tmp_path):
    file_path = tmp_path / "afile.txt"
    file_path.write_text("abc")
    f = File(str(file_path))
    assert os.path.isabs(f.get_full_path())
    assert os.path.isabs(f.get_full_dirname())
    assert f.get_full_dirname() == str(tmp_path)
    assert f.get_full_path().endswith("afile.txt")


def test_get_extension_and_filename_and_dirname(tmp_path):
    file_path = tmp_path / "foo.bar.txt"
    file_path.write_text("abc")
    f = File(str(file_path))
    assert f.get_extension() == "txt"
    assert f.get_filename() == "foo.bar"
    assert f.get_dirname() == str(tmp_path)
    assert f.get_full_dirname() == str(tmp_path)
    assert os.path.isabs(f.get_full_dirname())


def test_get_extension_no_extension(tmp_path):
    file_path = tmp_path / "filewithoutext"
    file_path.write_text("abc")
    f = File(str(file_path))
    assert f.get_extension() == ""
    assert f.get_filename() == "filewithoutext"


def test_create_dir_raises_if_cannot_create(monkeypatch, tmp_path):
    # Simulate os.makedirs failing to create the directory
    dir_path = tmp_path / "faildir"
    f = File(str(dir_path))

    def fake_makedirs(path, exist_ok=False):
        # Simulate makedirs doing nothing (directory not created)
        pass

    monkeypatch.setattr(os, "makedirs", fake_makedirs)
    # Ensure the directory does not exist before
    assert not dir_path.exists()
    with pytest.raises(FileNotFoundError) as excinfo:
        f.create_dir()
    assert "could not be created" in str(excinfo.value)
