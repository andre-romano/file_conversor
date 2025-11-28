# tests\backend\gui\_api\test_api_audio_check.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.audio.check import api_audio_check, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIAudioCheck:
    def test_check(self):
        url = FlaskRoute.get_url(api_audio_check)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.mp3"),
            ]),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
