# tests\backend\gui\_api\pdf\test_api_pdf_extract.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.extract import api_pdf_extract, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfExtract:
    def test_extract(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_pdf_extract)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.pdf"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "pages": "1",
            "password": "null",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_extracted.pdf").exists()
