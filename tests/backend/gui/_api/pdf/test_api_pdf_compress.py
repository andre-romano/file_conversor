# tests\backend\gui\_api\pdf\test_api_pdf_compress.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.compress import api_pdf_compress, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfCompress:
    def test_compress(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_pdf_compress)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.pdf"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "pdf-compression": "medium",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_compressed.pdf").exists()
