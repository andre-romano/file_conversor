# tests\backend\gui\_api\test_api_audio.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.audio.convert import api_audio_convert, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIAudioConvert:
    def test_convert(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_audio_convert)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.mp3"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "file-format": "m4a",
            "audio-bitrate": "192",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test.m4a").exists()
