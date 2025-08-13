import shlex
import subprocess
import sys

from pathlib import Path
from typer.testing import CliRunner

from file_conversor.cli.app_cmd import app_cmd
from file_conversor.config.state import State


DATA_PATH = Path(f"tests/.data")


class Test:
    RUNNER = CliRunner()

    @staticmethod
    def invoke(*cmd_list: str):

        result = Test.RUNNER.invoke(app_cmd, cmd_list)
        return result

    @staticmethod
    def run(*cmd_list: str):
        exe_cmd_list = shlex.split(f'"{sys.executable}" "{State.get_resources_folder() / "__main__.py"}"')

        cmd = exe_cmd_list.copy()
        cmd.extend(cmd_list)

        process = subprocess.run(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 )
        return process
