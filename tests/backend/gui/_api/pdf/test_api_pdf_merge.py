# tests\backend\gui\_api\pdf\test_api_pdf_merge.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.merge import api_pdf_merge, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfMerge:
    def test_merge(self, tmp_path: Path):
        files = [
            (DATA_PATH / "test.pdf", tmp_path / "test_merged.pdf"),
        ]

        url = FlaskRoute.get_url(api_pdf_merge)
        for in_file, out_file in files:
            reply = Test.flask_api(url, data={
                "input-files": str([
                    str(in_file),
                ]),
                "output-file": str(out_file),
                "password": "null",
                "overwrite-output": "true",
            })
            status = Test.flask_api_status(FlaskApiStatus(**reply))
            assert out_file.exists()
