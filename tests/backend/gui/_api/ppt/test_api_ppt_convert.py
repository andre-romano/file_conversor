# tests\backend\gui\_api\ppt\test_api_ppt_convert.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui._api.ppt.convert import api_ppt_convert, EXTERNAL_DEPENDENCIES

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPptConvert:
    def test_convert(self, tmp_path: Path):
        url = FlaskRoute.get_url(api_ppt_convert)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.pptx"),
            ]),
            "file-format": "pdf",
            "output-dir": str(tmp_path.resolve()),
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply), timeout=60)
        assert (tmp_path / "test.pdf").exists()
