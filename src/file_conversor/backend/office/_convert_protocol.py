
# src/file_conversor/backend/office/convert_protocol.py

from pathlib import Path
from typing import Protocol


class ConvertProtocol(Protocol):

    def convert(
        self,
        input_path: Path,
        output_path: Path,
    ) -> None:
        """
        Convert input file into an output file.

        :param input_path: Path to input file.
        :param output_path: Path to output file.
        :param file_processed_callback: Callback function called when a file is processed.

        :raises FileNotFoundError: if input file not found.
        """
        ...


__all__ = [
    "ConvertProtocol",
]
