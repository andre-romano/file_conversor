# src\file_conversor\tests\utils.py

from pathlib import Path
from typing import Iterable

from typer.testing import CliRunner

# user-provided imports
from file_conversor.cli import AppTyperGroup
from file_conversor.config.environment import Environment


app_cmd = AppTyperGroup().get_typer()

DATA_PATH = (Environment.get_resources_folder() / "tests" / ".data").resolve()


class TestTyper:
    RUNNER = CliRunner()

    @classmethod
    def dependencies_installed(cls, deps: Iterable[str]):
        import shutil
        return all(shutil.which(dep) is not None for dep in deps)

    @classmethod
    def invoke_test_help(cls, *cmd: str):
        result = cls.invoke(*cmd, "--help")
        expected = " ".join(cmd)
        print("EXP: ", expected, "- ACT:", result.stdout)
        assert expected in result.output
        assert result.exit_code == 0

    @staticmethod
    def get_format_params(out_path: Path):
        return ["-f", str(out_path.suffix[1:])]

    @staticmethod
    def get_out_dir_params(out_path: Path):
        return ["-od", str(out_path.parent)]

    @staticmethod
    def get_out_file_params(out_path: Path):
        return ["-of", str(out_path)]

    @staticmethod
    def invoke(*cmd_list: str):
        print(f"Args: {' '.join([f'"{c}"' for c in cmd_list])}")
        return TestTyper.RUNNER.invoke(app_cmd, cmd_list)

    @staticmethod
    def run(*cmd_list: str):
        import shlex
        import subprocess
        import sys

        exe_cmd_list = shlex.split(f'"{sys.executable}" -m "{Environment.get_app_name()}"')

        cmd = exe_cmd_list.copy()
        cmd.extend(cmd_list)
        print(f"Args: {' '.join([f'"{c}"' for c in cmd])}")

        return subprocess.run(cmd,  # noqa: S603
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 check=True
                                 )
