
# src/file_conversor/backend/office/convert_protocol.py

from pathlib import Path
from dataclasses import dataclass
from typing import Any, Callable, Protocol


class ConvertProtocol(Protocol):
    @dataclass
    class FilesDataModel:
        input_file: Path
        output_file: Path

    def convert(
        self,
        files: list[FilesDataModel],
        file_processed_callback: Callable[[Path], Any] | None = None,
    ):
        """
        Convert input file into an output file.

        :param files: List of FilesDataModel containing input and output file paths.    

        :raises FileNotFoundError: if input file not found.
        """
        ...


__all__ = [
    "ConvertProtocol",
]
