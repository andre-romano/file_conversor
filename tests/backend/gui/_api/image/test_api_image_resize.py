# tests\backend\gui\_api\image\test_api_image_resize.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.gui._api.image.resize import api_image_resize, EXTERNAL_DEPENDENCIES

from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageResize:
    def test_resize(self, tmp_path: Path):
        resampling_opts = list(PillowBackend.RESAMPLING_OPTIONS.keys())

        url = FlaskRoute.get_url(api_image_resize)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "image-scale": "1.5",
            "image-resampling": resampling_opts[0],
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_resized.png").exists()
