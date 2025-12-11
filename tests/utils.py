# tests\utils.py

import shlex
import shutil
import subprocess
import sys
import time

from pathlib import Path
from typing import Any, Iterable

from typer.testing import CliRunner

# user-provided imports
from file_conversor.backend.gui import WebApp
from file_conversor.backend.gui.flask_api_status import *

from file_conversor.cli import app_cmd
from file_conversor.config.environment import Environment


DATA_PATH = Path(f"tests/.data").resolve()


class Test:
    RUNNER = CliRunner()
    FAPP = WebApp.get_instance()._run_flask(testing=True)
    FCLIENT = FAPP.test_client()
    FRUNNER = FAPP.test_cli_runner()

    @classmethod
    def dependencies_installed(cls, deps: Iterable[str]):
        return all([shutil.which(dep) is not None for dep in deps])

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
        result = Test.RUNNER.invoke(app_cmd, cmd_list)
        return result

    @staticmethod
    def run(*cmd_list: str):
        exe_cmd_list = shlex.split(f'"{sys.executable}" "{Environment.get_resources_folder() / "__main__.py"}"')

        cmd = exe_cmd_list.copy()
        cmd.extend(cmd_list)
        print(f"Args: {' '.join([f'"{c}"' for c in cmd])}")

        process = subprocess.run(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 )
        return process

    @staticmethod
    def flask_webpage(
        url: str,
        data: dict[str, Any] | None = None,
        status_code: int = 200,
    ) -> str:
        """
        Check Flask webpage.

        :param url: Webpage URL.
        :param status_code: Expected HTTP status code (default is 200).

        :return: Webpage content as a string.
        """
        response = Test.FCLIENT.get(url, data=data or {})
        reply = response.data.decode("utf-8")
        assert response.status_code == status_code
        assert "<!DOCTYPE html>" in reply
        assert "</html>" in reply
        return reply

    @staticmethod
    def flask_api(
        url: str,
        method: str = "POST",
        data: dict[str, Any] | None = None,
        status_code: int = 200,
    ):
        """
        Check Flask API endpoint.

        :param url: API endpoint URL.
        :param status_code: Expected HTTP status code (default is 200).
        :param data: Data to send with the request (default is None).

        :return: JSON response as a dictionary.
        """
        data = {
            k: str(v)
            for k, v in (data or {}).items()
        }

        if method.upper() == "GET":
            response = Test.FCLIENT.get(url, query_string=data)
        else:
            response = Test.FCLIENT.post(url, data=data)

        json_reply = response.get_json() or {}
        # print(f"url: {url} - data: {data}\n- JSON reply: {json_reply}")
        assert json_reply['exception'] == ''

        assert response.status_code == status_code
        return json_reply

    @staticmethod
    def flask_api_status(
        fapi_status: FlaskApiStatus | int | str,
        timeout: float = 30,  # in sec
        sleep_time: float = 0.100,  # in sec
    ):
        retry = timeout / sleep_time
        while retry > 0:
            status_id = fapi_status.get_id() if isinstance(fapi_status, FlaskApiStatus) else str(fapi_status)
            reply = Test.flask_api("/api/status", method='GET', data={
                "id": status_id,
            })
            status = FlaskApiStatus(**reply)
            status_completed = FlaskApiStatusCompleted(status.get_id())
            status_processing = FlaskApiStatusProcessing(status.get_id())
            assert status.get_exception() == ""
            assert (status == status_completed or status == status_processing)
            if status == status_completed:
                return status
            time.sleep(sleep_time)
            retry -= 1
        raise RuntimeError("Flask status API timeout")
