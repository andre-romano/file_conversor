# tests\backend\gui\_api\image\test_api_image_blur.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.gui._api.image.blur import api_image_blur, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageBlur:
    def test_blur(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_image_blur)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "radius": "2",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_blurred.png").exists()
