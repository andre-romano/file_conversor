# tests\backend\gui\_api\image\test_api_image_enhance.py

import platform
import pytest

from pathlib import Path
from flask import url_for


# user-provided imports
from file_conversor.backend.gui._api.image.enhance import api_image_enhance, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageEnhance:
    def test_enhance(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_image_enhance)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "color": "1.2",
            "brightness": "1.2",
            "contrast": "1.2",
            "sharpness": "1.2",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_enhanced.png").exists()
