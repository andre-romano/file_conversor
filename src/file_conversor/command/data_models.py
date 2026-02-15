# src\file_conversor\command\_data_models.py

from pathlib import Path
from typing import Callable

from pydantic import BaseModel, model_validator

# user-provided modules
from file_conversor.command.progress_manager import ProgressManager
from file_conversor.config import Log, get_translation
from file_conversor.utils.formatters import get_output_file


LOG = Log.get_instance()

logger = LOG.getLogger(__name__)
_ = get_translation()


class FilesDataModel(BaseModel):
    input_files: list[Path]
    output_file: Path
    overwrite_output: bool

    @classmethod
    def expand_and_normalize(cls, path: Path | str) -> Path:
        import os

        # Expand environment variables and resolve paths
        return Path(os.path.expandvars(path)).resolve()

    @model_validator(mode="after")
    def _check_model(self):
        # Expand environment variables and resolve paths
        for idx in range(len(self.input_files)):
            self.input_files[idx] = self.expand_and_normalize(self.input_files[idx])

        for input_file in self.input_files:
            if not input_file.exists():
                raise FileNotFoundError(f"Input file '{input_file}' does not exist")

        self.output_file = self.expand_and_normalize(self.output_file)
        if self.output_file.exists() and not self.overwrite_output:
            raise FileExistsError(f"Output file '{self.output_file}' already exists and overwrite mode is DISABLED")

        for input_file in self.input_files:
            if input_file == self.output_file:
                raise RuntimeError("Input file and output file cannot be the same")
        return self

    def execute(
        self,
        *steps_callbacks: Callable[['FilesDataModel', Callable[[float], float]], None],
    ):
        """
        Execute processing with callbacks.

        :param steps_callbacks: Callbacks for each step. Each callback receives the current InOutFileDataModel and progress_callback (calculates progress 0-100 for file).
        """
        progress_mgr = ProgressManager(steps_per_file=len(steps_callbacks))
        for step_callback in steps_callbacks:
            step_callback(self, progress_mgr.get_progress)
            progress_mgr.next_step()


class FileDataModel(BaseModel):
    input_file: Path
    output_file: Path
    overwrite_output: bool

    @classmethod
    def expand_and_normalize(cls, path: Path | str) -> Path:
        return FilesDataModel.expand_and_normalize(path)

    @model_validator(mode="after")
    def _check_model(self):
        # Expand environment variables and resolve paths
        self.input_file = self.expand_and_normalize(self.input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file '{self.input_file}' does not exist")

        self.output_file = self.expand_and_normalize(self.output_file)
        if self.output_file.exists() and not self.overwrite_output:
            raise FileExistsError(f"Output file '{self.output_file}' already exists and overwrite mode is DISABLED")
        if self.input_file == self.output_file:
            raise RuntimeError("Input file and output file cannot be the same")

        return self

    def execute(
        self,
        *steps_callbacks: Callable[['FileDataModel', Callable[[float], float]], None],
    ):
        """
        Execute processing with callbacks.

        :param steps_callbacks: Callbacks for each step. Each callback receives the current InOutFileDataModel and progress_callback (calculates progress 0-100 for file).
        """
        progress_mgr = ProgressManager(steps_per_file=len(steps_callbacks))
        for step_callback in steps_callbacks:
            step_callback(self, progress_mgr.get_progress)
            progress_mgr.next_step()


class BatchFilesDataModel(BaseModel):
    input_files: list[Path]
    output_dir: Path
    overwrite_output: bool
    out_stem: str = ""
    out_suffix: str | None = None

    @classmethod
    def _get_step_file(cls, path: Path, step_idx: int) -> Path:
        return path.with_stem(path.stem + f"_step{step_idx}")

    def __len__(self):
        return len(self.input_files)

    @model_validator(mode="after")
    def _check_model(self):
        # validate input files
        if not self.input_files:
            raise RuntimeError("No input files provided")

        # validate output path
        self.output_dir = FileDataModel.expand_and_normalize(self.output_dir)
        if self.output_dir.exists() and not self.output_dir.is_dir():
            raise NotADirectoryError(f"Output path '{self.output_dir}' is not a directory")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        if not self.output_dir.exists():
            raise OSError(f"Output path '{self.output_dir}' does not exist")

        return self

    def get_iterator(self):
        for input_file in self.input_files:
            # Determine output file path
            output_file = get_output_file(
                input_file=input_file,
                output_dir=self.output_dir,
                out_stem=self.out_stem,
                out_suffix=self.out_suffix,
            )

            yield FileDataModel(
                input_file=input_file,
                output_file=output_file,
                overwrite_output=self.overwrite_output,
            )

    def get_list(self):
        return list(self.get_iterator())

    def execute(
        self,
        *steps_callbacks: Callable[[FileDataModel, Callable[[float], float]], None],
    ):
        """
        Execute batch processing with callbacks.

        :param steps_callbacks: Callbacks for each step. Each callback receives the current InOutFileDataModel and progress_callback (calculates progress 0-100 for file).
        """
        logger.info(f"[bold]{_('Processing files')}[/] ...")
        progress_mgr = ProgressManager(len(self.input_files), steps_per_file=len(steps_callbacks))
        for datamodel in self.get_iterator():
            for idx, step_callback in enumerate(steps_callbacks):
                step_datamodel = FileDataModel(
                    input_file=datamodel.input_file if idx == 0 else self._get_step_file(datamodel.output_file, idx - 1),
                    output_file=datamodel.output_file if idx == (len(steps_callbacks) - 1) else self._get_step_file(datamodel.output_file, idx),
                    overwrite_output=datamodel.overwrite_output,
                )
                step_callback(step_datamodel, progress_mgr.get_progress)
                progress_mgr.next_step()
                if idx > 0:
                    step_datamodel.input_file.unlink(missing_ok=True)  # remove temp file


__all__ = [
    "FilesDataModel",
    "FileDataModel",
    "BatchFilesDataModel",
]
