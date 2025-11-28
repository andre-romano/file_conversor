# tests\backend\gui\_api\hash\test_api_hash_create_check.py

import platform
import pytest
import shutil

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.hash.create import api_hash_create, EXTERNAL_DEPENDENCIES
from file_conversor.backend.gui._api.hash.check import api_hash_check

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIHashCreateCheck:
    def test_create_check(self, tmp_path: Path):
        input_file = "test.png"
        output_file = "test.sha256"

        shutil.copy2(DATA_PATH / input_file, tmp_path / input_file)
        assert (tmp_path / input_file).exists()

        url = FlaskRoute.get_url(api_hash_create)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(tmp_path / input_file),
            ]),
            "output-file": str(tmp_path / output_file),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / output_file).exists()

        url = FlaskRoute.get_url(api_hash_check)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(tmp_path / output_file),
            ]),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
