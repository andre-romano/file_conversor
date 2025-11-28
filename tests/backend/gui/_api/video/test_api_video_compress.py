# tests\backend\gui\_api\video\test_api_video_compress.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.video.compress import api_video_compress, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIVideoCompress:
    def test_compress(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_video_compress)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.mp4"),
            ]),
            "output-dir": str(tmp_path.resolve()),

            'file-format': "mp4",
            'target-size': "0",

            'video-encoding-speed': "medium",
            'video-quality': "medium",

            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_compressed.mp4").exists()
