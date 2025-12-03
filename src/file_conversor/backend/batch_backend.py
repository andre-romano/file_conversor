# src\file_conversor\backend\batch_backend.py

"""
This module provides functionalities for barch file processing using this app.
"""

import shlex
import os
import subprocess
import json

from pathlib import Path

from rich import print
from rich.progress import Progress

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.config import Environment, Configuration, Log
from file_conversor.config.locale import get_translation

from file_conversor.utils.rich_utils import DummyProgress

# get app config
CONFIG = Configuration.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class BatchBackend(AbstractBackend):
    """Class to provide batch file processing, using pipelines"""
    SUPPORTED_IN_FORMATS = {}
    SUPPORTED_OUT_FORMATS = {}

    CONFIG_FILENAME = ".config_fc.json"

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        pipeline_folder: str
    ):
        """
        Initialize the Batch backend.
        """
        super().__init__()

        self._pipeline_path = Path(os.path.expandvars(pipeline_folder)).resolve()
        self._config_file = self._pipeline_path / self.CONFIG_FILENAME

        self._config_data = []

        self._stage_len = 0
        self._stage_num = 1
        self._stage_prev = self._pipeline_path

    def add_stage(self, out_dir: str, command: str):
        stage = f"{self._stage_num}_{out_dir}"
        stage_path = (self._pipeline_path / stage).resolve()
        stage_path.mkdir(exist_ok=True)

        self._config_data.append({
            "in_dir": self._stage_prev,
            "out_dir": stage_path,
            "command": command,
        })
        self._stage_num += 1
        self._stage_prev = stage_path
        logger.info(f"{_('Pipeline stage created at')} '{stage_path}'")

    def save_config(self,):
        self._pipeline_path.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(json.dumps(self._config_data, indent=2, sort_keys=True))
        logger.info(f"{_('Config file saved at')} '{self._config_file}'")

    def load_config(self,):
        """
        Load configuration file

        :raises RuntimeError: config file does not exist.
        """
        if not self._config_file.exists():
            raise RuntimeError(f"{_('Config file')} '{self._pipeline_path}' {_('does not exist')}")
        logger.info(f"{_('Loading')} '{self._config_file}' ...")
        with open(self._config_file, "r") as f:
            self._config_data = json.load(f)
        self._stage_len = len(self._config_data)
        logger.info(f"{_('Found')} {self._stage_len} {_('stages')}")

    def execute(self, progress: Progress | DummyProgress):
        """
        Executes the batch pipeline

        :raises subprocess.CalledProcessError: if a stage failes.
        """
        task = progress.add_task(f"{_('Processing stage')}", total=self._stage_len)
        for i, stage in enumerate(self._config_data):
            progress.update(task, description=f"{_('Processing stage')} {i + 1}/{self._stage_len}")
            self._execute_stage(progress=progress, **stage)
            progress.update(task, completed=i + 1)

    def _execute_stage(self, progress: Progress | DummyProgress, in_dir: str, out_dir: str, command: str):
        """
        Process a pipeline stage

        :raises subprocess.CalledProcessError: if a stage failes
        """
        input_path = Path(in_dir)
        output_path = Path(out_dir)
        cmd_template = str(command)

        logger.info(f"{_('Executing batch stage')} '{out_dir}' ...")
        total_files = sum(1 for _ in input_path.glob("*"))
        task = progress.add_task(f"{_('Stage')} '{output_path.name}' - {_('Processing files')}", total=total_files)
        for i, in_path in enumerate(input_path.glob("*")):
            # ignore folders and config file
            if in_path.is_dir() or in_path.name == self.CONFIG_FILENAME:
                continue
            # execute cmd
            try:
                cmd_list = self._gen_cmd_list(in_path, in_path=in_path, out_path=output_path, cmd_template=cmd_template)
                logger.debug(f"Command list: '{cmd_list}'")
                process = Environment.run(*cmd_list)
                logger.debug(f"Processing file '{in_path}': [bold green]{_('SUCCESS')}[/] ({process.returncode})")
            except Exception as e:
                logger.error(f"Processing file '{in_path}': [bold red]{_('FAILED')}[/]")
                logger.error(f"{str(e)}")
                if isinstance(e, subprocess.CalledProcessError):
                    logger.error(f"Stdout:\n{e.stdout}")
                    logger.error(f"Stderr:\n{e.stderr}")
                self._clean_stage(output_path)
                raise
            finally:
                progress.update(task, completed=i + 1)
        # success, clean input_path
        self._clean_stage(input_path)
        progress.update(task, total=100, completed=100)
        logger.info(f"{_('Finished batch stage')} '{out_dir}'")

    def _clean_stage(self, dir_path: Path):
        """Clean files inside folder"""
        logger.debug(f"Cleaning files from folder '{dir_path}' ...")
        for path in dir_path.glob("*"):
            if path.is_file() and path.name != self.CONFIG_FILENAME:
                path.unlink()

    def _gen_cmd_list(self, input_path: Path, in_path: Path, out_path: Path, cmd_template: str):
        """Creates the command list based on cmd_template"""
        cmd_list = []
        for cmd in shlex.split(f"{Environment.get_executable()} {cmd_template}"):
            # replace placeholders
            cmd = cmd.replace("{{in_file_path}}", f"{input_path.resolve()}")
            cmd = cmd.replace("{{in_file_name}}", f"{input_path.with_suffix("").name}")
            cmd = cmd.replace("{{in_file_ext}}", f"{input_path.suffix[1:].lower()}")
            cmd = cmd.replace("{{in_dir}}", f"{in_path}")
            cmd = cmd.replace("{{out_dir}}", f"{out_path}")
            # normalize paths
            if "/" in cmd or "\\" in cmd:
                cmd = os.path.normpath(cmd)
            cmd_list.append(cmd)
        return cmd_list


__all__ = [
    "BatchBackend",
]
