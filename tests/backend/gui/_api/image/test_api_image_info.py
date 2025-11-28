# tests\backend\gui\_api\image\test_api_image_info.py

import platform
import pytest

from pathlib import Path
from flask import url_for


# user-provided imports
from file_conversor.backend.gui._api.image.info import api_image_info, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageInfo:
    def test_info(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_image_info)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert "PNG" in status.get_message()
