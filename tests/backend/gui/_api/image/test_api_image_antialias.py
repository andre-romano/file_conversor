# tests\backend\gui\_api\image\test_api_image_antialias.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.image import PillowBackend

from file_conversor.backend.gui._api.image.antialias import api_image_antialias, EXTERNAL_DEPENDENCIES
from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageAntialias:
    def test_antialias(self, tmp_path: Path):
        algorithms = list(PillowBackend.AntialiasAlgorithm.get_dict().keys())

        url = FlaskRoute.get_url(api_image_antialias)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(DATA_PATH / "test.png"),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "radius": "3",
            "algorithm": algorithms[0],
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (tmp_path / "test_antialiased.png").exists()
