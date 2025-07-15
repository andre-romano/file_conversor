import pytest

from unittest.mock import patch, MagicMock
from backend.backend_abstract import BackendAbstract

# Patch the File class in the backend_abstract module


@patch("backend.backend_abstract.File")
def test_init_sets_input_and_output_and_options(mock_file):
    # Setup mocks
    mock_file.return_value.is_file.return_value = True
    mock_file.return_value.get_dirname.return_value = "some_dir"
    mock_file.return_value.create_dir.return_value = None

    backend = BackendAbstract("input.txt", "output.txt", opt1=1, opt2="val")
    assert backend.input_file == "input.txt"
    assert backend.output_file == "output.txt"
    assert backend.options == {"opt1": 1, "opt2": "val"}


@patch("backend.backend_abstract.File")
def test_set_input_raises_if_file_not_exists(mock_file):
    mock_file.return_value.is_file.return_value = False
    with pytest.raises(FileNotFoundError):
        BackendAbstract("missing.txt", "output.txt")


@patch("backend.backend_abstract.File")
def test_set_output_creates_dir_if_needed(mock_file):
    mock_file.return_value.is_file.return_value = True
    mock_file.return_value.get_dirname.return_value = "dir"
    mock_file.return_value.create_dir = MagicMock()

    BackendAbstract("input.txt", "output.txt")
    mock_file.return_value.create_dir.assert_called_once()


@patch("backend.backend_abstract.File")
def test_set_output_no_dir_creation_if_no_dir(mock_file):
    mock_file.return_value.is_file.return_value = True
    mock_file.return_value.get_dirname.return_value = ""
    mock_file.return_value.create_dir = MagicMock()

    BackendAbstract("input.txt", "output.txt")
    mock_file.return_value.create_dir.assert_not_called()


@patch("backend.backend_abstract.File")
def test_set_options_updates_options(mock_file):
    mock_file.return_value.is_file.return_value = True
    mock_file.return_value.get_dirname.return_value = ""
    backend = BackendAbstract("input.txt", "output.txt")
    backend.set_options(a=1, b=2)
    assert backend.options == {"a": 1, "b": 2}
    backend.set_options(b=3, c=4)
    assert backend.options == {"a": 1, "b": 3, "c": 4}


@patch("backend.backend_abstract.File")
def test_execute_not_implemented(mock_file):
    mock_file.return_value.is_file.return_value = True
    mock_file.return_value.get_dirname.return_value = ""
    backend = BackendAbstract("input.txt", "output.txt")
    with pytest.raises(NotImplementedError):
        backend.execute()
