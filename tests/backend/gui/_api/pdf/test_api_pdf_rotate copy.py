# tests\backend\gui\_api\pdf\test_api_pdf_split.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.split import api_pdf_split, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfSplit:
    def test_split(self, tmp_path: Path):
        files = [
            (DATA_PATH / "test.pdf", tmp_path / "test_1.pdf"),
        ]

        url = FlaskRoute.get_url(api_pdf_split)
        for in_file, out_file in files:
            reply = Test.flask_api(url, data={
                "input-files": str([
                    str(in_file),
                ]),
                "output-dir": str(out_file.parent),
                "password": "null",
                "overwrite-output": "true",
            })
            status = Test.flask_api_status(FlaskApiStatus(**reply))
            assert out_file.exists()
