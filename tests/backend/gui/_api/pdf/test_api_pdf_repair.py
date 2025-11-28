# tests\backend\gui\_api\pdf\test_api_pdf_repair.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.pdf.repair import api_pdf_repair, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfRepair:
    def test_repair(self, tmp_path: Path):
        files = [
            (DATA_PATH / "test.pdf", tmp_path / "test_repaired.pdf"),
        ]

        url = FlaskRoute.get_url(api_pdf_repair)
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
