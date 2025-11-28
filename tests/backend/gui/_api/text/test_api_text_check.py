# tests\backend\gui\_api\text\test_api_text_check.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.text.check import api_text_check, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPITextCheck:
    def test_check(self):
        url = FlaskRoute.get_url(api_text_check)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.json"),
            ]),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
