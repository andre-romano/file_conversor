# tests\backend\gui\_api\test_api_audio.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.audio.info import api_audio_info, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIAudioInfo:
    def test_info(self):
        url = FlaskRoute.get_url(api_audio_info)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.mp3"),
            ]),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert status.get_message() != ""
