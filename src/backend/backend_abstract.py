
# src/backend/backend_abstract.py

from utils.file import File


class BackendAbstract:
    """
    This abstract class defines the interface for backend implementations.
    Subclasses must implement the input, output, and execute methods.
    """

    def __init__(self, input_file: str, output_file: str, **kwargs):
        """
        Initialize the backend with input and output files, with kwargs options.

        :param input_file: Input file path.
        :param output_file: Output file path.
        :param kwargs: Option flags.

        :raises FileNotFoundError: If the input file does not exist, or output directory could not be created.
        """
        self.input_file = ""
        self.output_file = ""
        self.options = {}

        self._set_input(input_file)
        self._set_output(output_file)
        self.set_options(**kwargs)

    def _set_input(self, input_file: str):
        """
        Set the input file.

        :param input_file: Input file path.

        :raises FileNotFoundError: If the input file does not exist.
        """
        if not File(input_file).is_file():
            raise FileNotFoundError(
                f"Input file '{input_file}' does not exist.")
        self.input_file = input_file
        return self

    def _set_output(self, output_file: str):
        """
        Set the output file.

        :param output_file: Output file path.

        :raises FileNotFoundError: If the output directory could not be created.
        """
        dir = File(output_file).get_dirname()
        if dir:
            File(dir).create_dir()

        self.output_file = output_file
        return self

    def set_options(self, **kwargs):
        """
        Set options flags.

        :param kwargs: Options dict[str, Any].
        """
        self.options.update(kwargs)

    def execute(self) -> tuple[str, str]:
        """
        Execute the backend operation.
        This method should be implemented by subclasses.

        :return: A tuple containing the standard output and error messages.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses")
