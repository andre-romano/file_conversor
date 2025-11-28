# tests\backend\gui\_api\pdf\test_api_pdf_convert.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.convert import api_pdf_convert, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfConvert:
    def test_convert(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_pdf_convert)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.pdf"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "file-format": "png",
            "image-dpi": "200",
            "password": "null",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_1.png").exists()
