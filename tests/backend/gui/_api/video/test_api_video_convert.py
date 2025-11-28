# tests\backend\gui\_api\video\test_api_video_convert.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.video.convert import api_video_convert, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIVideoConvert:
    def test_convert(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_video_convert)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH.resolve() / "test.mp4"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "file-format": "mkv",

            "audio-bitrate": "0",
            "video-bitrate": "0",

            "audio-codec": "",
            "video-codec": "",

            "video-encoding-speed": "medium",
            "video-quality": "medium",

            "resolution": "",
            "fps": "",

            "brightness": "1.0",
            "contrast": "1.0",
            "color": "1.0",
            "gamma": "1.0",

            "rotation": "0",
            "mirror-axis": "",

            "deshake": "off",
            "unsharp": "off",

            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test.mkv").exists()
