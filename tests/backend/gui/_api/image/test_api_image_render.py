# tests\backend\gui\_api\image\test_api_image_render.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.gui._api.image.render import api_image_render, EXTERNAL_DEPENDENCIES

from file_conversor.backend.image import PillowBackend, Img2PDFBackend

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageRender:
    def test_render(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_image_render)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.svg"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "file-format": "jpg",
            "image-dpi": "200",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test.jpg").exists()
