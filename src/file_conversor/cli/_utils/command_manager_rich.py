# src\file_conversor\cli\command_manager_rich.py

from pathlib import Path
from typing import Any, Callable, List

# user-provided
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import get_output_file

from file_conversor.cli._utils.progress_manager_rich import ProgressManagerRich

_ = get_translation()


class CommandManagerRich:

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

    def run(self, callback: Callable[[Path, Path, ProgressManagerRich], Any], out_stem: str | None = None, out_suffix: str | None = None):
        """
        Run batch command

        :param callback: lambda input_file, output_file, progress_mgr
        """
        with ProgressManagerRich(len(self._input_files), total_steps_per_file=self._steps) as progress_mgr:
            for input_file in self._input_files:
                output_file = self._output_dir / get_output_file(input_file, stem=out_stem, suffix=out_suffix)
                if not self._overwrite and output_file.exists():
                    raise FileExistsError(f"{_("File")} '{output_file}' {_("exists")}. {_("Use")} 'file_conversor -oo' {_("to overwrite")}.")

                callback(input_file, output_file, progress_mgr)


__all__ = [
    "CommandManagerRich",
]
