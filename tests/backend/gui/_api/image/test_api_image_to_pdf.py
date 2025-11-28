# tests\backend\gui\_api\image\test_api_image_to_pdf.py

import platform
import pytest

from pathlib import Path

# user-provided imports
from file_conversor.backend.gui._api.image.to_pdf import api_image_to_pdf, EXTERNAL_DEPENDENCIES

from file_conversor.backend.image import Img2PDFBackend

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIImageToPdf:
    def test_to_pdf(self, tmp_path: Path):
        fit_opts = list(Img2PDFBackend.FIT_MODES.keys())
        page_sz_opts = list(Img2PDFBackend.PAGE_LAYOUT.keys())

        input_file = DATA_PATH / "test.png"
        output_file = tmp_path / "test.pdf"

        url = FlaskRoute.get_url(api_image_to_pdf)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(input_file),
            ]),
            "output-file": str(output_file),
            "image-dpi": "200",
            "image-fit": fit_opts[0],
            "image-page-size": page_sz_opts[0],
            "image-set-metadata": "off",
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert (output_file).exists()
