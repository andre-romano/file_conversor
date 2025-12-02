# src\file_conversor\utils\command_manager.py

from pathlib import Path
from typing import Any, Callable, List

# user-provided
from file_conversor.config.locale import get_translation

from file_conversor.utils.progress_manager import ProgressManager

_ = get_translation()


class CommandManager:
    @staticmethod
    def get_output_file(
            output_file: str | Path,
            stem: str | None = None,
            suffix: str | None = None,
    ):
        """
        Get output file based on input
        """
        output_file = Path(output_file)
        output_name = output_file.with_stem(f"{output_file.with_suffix("").name}{stem or ""}")
        output_name = output_name.with_suffix(suffix if suffix is not None else output_file.suffix)
        return Path(output_name.name)

    def __init__(self, input_files: List[str] | List[Path] | str | Path, output_dir: Path, overwrite: bool, steps: int = 1) -> None:
        super().__init__()
        self._overwrite = overwrite
        self._output_dir = output_dir
        self._steps = steps
        self._input_files: list[Path] = []

        if isinstance(input_files, list):
            self._input_files.extend([Path(f) for f in input_files])
        else:
            self._input_files.append(Path(input_files))

    def run(self, callback: Callable[[Path, Path, ProgressManager], Any], out_stem: str | None = None, out_suffix: str | None = None):
        """
        Run batch command

        :param callback: lambda input_file, output_file, progress_mgr
        """
        with ProgressManager(len(self._input_files), total_steps_per_file=self._steps) as progress_mgr:
            for input_file in self._input_files:
                output_file = self._output_dir / self.get_output_file(input_file, stem=out_stem, suffix=out_suffix)
                if not self._overwrite and output_file.exists():
                    raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")

                callback(input_file, output_file, progress_mgr)


__all__ = [
    "CommandManager",
]
