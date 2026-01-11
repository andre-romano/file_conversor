# src\file_conversor\backend\batch_backend.py

"""
This module provides functionalities for barch file processing using this app.
"""

import shlex
import os
import subprocess

from pathlib import Path
from typing import Any, Callable, Self

from pydantic import BaseModel
from rich import print

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.config import Environment, Configuration, Log
from file_conversor.config.locale import get_translation

# get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)

_PIPELINE_CONFIG_FILENAME = ".config_fc.json"
"""Pipeline configuration filename"""


def _clean_dir(dir_path: Path):
    """
    Clean files inside folder

    :param dir_path: directory path
    """
    logger.debug(f"Cleaning files from folder '{dir_path}' ...")
    for path in dir_path.glob("*"):
        if path.is_file() and path.name != _PIPELINE_CONFIG_FILENAME:
            path.unlink()


class StageConfigDataModel(BaseModel):
    in_dir: Path
    out_dir: Path
    command: str

    @staticmethod
    def help_template():
        """ Get help template for stage creation """

        return f"""
{_('Creates a pipeline stage.')}

{_('Placeholders available for commands')}:

- **{{in_file_path}}**: {_('Replaced by the first file path found in pipeline stage.')}

    - Ex: C:/Users/Alice/Desktop/pipeline_name/my_file.jpg

- **{{in_file_name}}**: {_('The name of the input file.')}

    - Ex: my_file

- **{{in_file_ext}}**: {_('The extension of the input file.')}

    - Ex: jpg

- **{{in_dir}}**: {_('The directory of the input path (previous pipeline stage).')}

    - Ex: C:/Users/Alice/Desktop/pipeline_name

- **{{out_dir}}**: {_('The directory of the output path (current pipeline stage).')}

    - Ex: C:/Users/Alice/Desktop/pipeline_name/0_image_convert
"""

    def _gen_cmd_list(self, inputfile_path: Path):
        """
        Creates the command list based on cmd_template

        :param inputfile_path: input file path

        :return: list of command arguments
        """
        cmd_list: list[str] = []
        for cmd in shlex.split(f"{Environment.get_executable()} {self.command}"):
            # replace placeholders
            cmd = cmd.replace(f"{{in_file_path}}", f"{inputfile_path.resolve()}")
            cmd = cmd.replace(f"{{in_file_name}}", f"{inputfile_path.with_suffix("").name}")
            cmd = cmd.replace(f"{{in_file_ext}}", f"{inputfile_path.suffix[1:].lower()}")
            cmd = cmd.replace(f"{{in_dir}}", f"{self.in_dir.resolve()}")
            cmd = cmd.replace(f"{{out_dir}}", f"{self.out_dir.resolve()}")
            # normalize paths
            if "/" in cmd or "\\" in cmd:
                cmd = os.path.normpath(cmd)
            cmd_list.append(cmd)
        return cmd_list

    def execute(
        self,
        progress_callback: Callable[[float], Any] = lambda p: p,
    ) -> None:
        """
        Process a pipeline stage

        :raises subprocess.CalledProcessError: if a stage failes
        """
        logger.info(f"{_('Executing batch stage')} '{self.out_dir}' ...")
        self.out_dir.mkdir(parents=True, exist_ok=True)

        total_files = sum(1 for _ in self.in_dir.glob("*"))
        for i, in_path in enumerate(self.in_dir.glob("*")):
            # update progress
            progress = float(i) / total_files * 100.0
            progress_callback(progress)

            # ignore folders and config file
            if in_path.is_dir() or in_path.name == _PIPELINE_CONFIG_FILENAME:
                continue

            # execute cmd
            try:
                cmd_list = self._gen_cmd_list(in_path)
                logger.debug(f"Command list: '{cmd_list}'")
                process = Environment.run(*cmd_list)

                logger.debug(f"Processing file '{in_path}': [bold green]{_('SUCCESS')}[/] ({process.returncode})")
            except Exception as e:
                logger.error(f"Processing file '{in_path}': [bold red]{_('FAILED')}[/]")
                logger.error(f"{str(e)}")
                if isinstance(e, subprocess.CalledProcessError):
                    logger.error(f"Stdout:\n{e.stdout}")
                    logger.error(f"Stderr:\n{e.stderr}")
                _clean_dir(self.out_dir)
                raise
        # success, clean input_path
        _clean_dir(self.in_dir)

        # final progress update
        progress_callback(100.0)
        logger.info(f"{_('Finished batch stage')} '{self.out_dir}'")


class PipelineConfigDataModel(BaseModel):
    folder: Path
    stages: list[StageConfigDataModel]

    def add_stage(self, out_dir: str, command: str):
        stage: str = f"{len(self.stages)}_{out_dir}"

        stage_path: Path = (self.folder / stage).resolve()
        stage_path.mkdir(exist_ok=True)

        stage_prev_path: Path = self.stages[-1].out_dir if self.stages else self.folder

        self.stages.append(StageConfigDataModel(
            in_dir=stage_prev_path,
            out_dir=stage_path,
            command=command,
        ))
        logger.info(f"{_('Pipeline stage created at')} '{stage_path}'")


class BatchBackend(AbstractBackend):
    """Class to provide batch file processing, using pipelines"""
    SUPPORTED_IN_FORMATS = {}
    SUPPORTED_OUT_FORMATS = {}

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        pipeline_folder: Path | str,
    ):
        """
        Initialize the Batch backend.
        """
        super().__init__()

        pipeline_dir_path = Path(os.path.expandvars(pipeline_folder)).resolve()
        pipeline_dir_path.mkdir(parents=True, exist_ok=True)

        self._pipeline_path: Path = pipeline_dir_path / _PIPELINE_CONFIG_FILENAME

        self._pipeline = PipelineConfigDataModel(
            folder=pipeline_dir_path,
            stages=[],
        )

    @property
    def pipeline(self) -> PipelineConfigDataModel:
        """Get the stages list"""
        return self._pipeline

    def save_config(self) -> None:
        self._pipeline_path.write_text(
            self._pipeline.model_dump_json(indent=2),
            encoding="utf-8",
        )
        logger.info(f"{_('Config file saved at')} '{self._pipeline_path}'")

    def load_config(self) -> None:
        """
        Load configuration file

        :raises RuntimeError: config file does not exist.
        """
        if not self._pipeline_path.exists():
            raise RuntimeError(f"{_('Config file')} '{self._pipeline_path}' {_('does not exist')}")

        logger.info(f"{_('Loading')} '{self._pipeline_path}' ...")
        self._pipeline = PipelineConfigDataModel.model_validate_json(
            self._pipeline_path.read_text(encoding="utf-8"),
        )

        logger.info(f"{_('Found')} {len(self._pipeline.stages)} {_('stages')}")


__all__ = [
    "BatchBackend",
]
