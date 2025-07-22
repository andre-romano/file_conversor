
import os


class File:
    """
    File is a utility class for handling file operations.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the File object with a given path.

        :param path: The path to the file or directory.
        :raises ValueError: If the path is not specified or is not a string.
        """
        super().__init__()

        if not path or not isinstance(path, str):
            raise ValueError("Path must be specified (string)")
        self.path = path

    def is_file(self) -> bool:
        """
        Check if a file exists at the given path.

        :return: True if the file exists, False otherwise.
        """
        return os.path.isfile(self.path)

    def is_dir(self) -> bool:
        """
        Check if a dir exists at the given path.

        :return: True if the dir exists, False otherwise.
        """
        return os.path.isdir(self.path)

    def create_dir(self) -> None:
        """
        Create a directory if it does not exist.

        :raises FileExistsError: If the path is a file.
        :raises FileNotFoundError: If the directory could not be created, or if path is a file.
        """
        if os.path.isfile(self.path):
            raise FileExistsError(f"Path '{self.path}' is a file, not a directory.")

        os.makedirs(self.path, exist_ok=True)
        if not os.path.isdir(self.path):
            raise FileNotFoundError(f"Directory '{self.path}' could not be created.")

    def check_supported_format(self, supported_formats: list | dict):
        """
        Check if the file has a supported format.

        :param supported_formats: List or dict of supported file formats.

        :raises ValueError: If the file format is not supported.
        """
        extension = self.get_extension()
        if extension not in supported_formats:
            raise ValueError(f"Unsupported format: {extension}. Supported formats are: {', '.join(supported_formats)}")

    def get_extension(self) -> str:
        """
        Get the file extension.

        :return: The file extension.
        """
        return (os.path.splitext(self.path)[1])[1:].lower()

    def get_filename(self) -> str:
        """
        Get the file name without the extension.

        :return: The file name without the extension.
        """
        return os.path.splitext(os.path.basename(self.path))[0]

    def get_dirname(self) -> str:
        """
        Get the directory name of the file.

        :return: The directory name.
        """
        return os.path.dirname(self.path)

    def get_full_dirname(self) -> str:
        """
        Get the full absolute path of the directory.

        :return: The full absolute path of the directory.
        """
        return os.path.abspath(self.get_dirname())

    def get_full_path(self) -> str:
        """
        Get the full absolute path of the file.

        :return: The full absolute path of the file.
        """
        return os.path.abspath(self.path)
