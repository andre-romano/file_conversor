# tests\backend\gui\_api\image\test_api_image_compress.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.image.compress import api_image_compress, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageCompress:
    def test_compress(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_image_compress)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "image-quality": "90",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_compressed.png").exists()
