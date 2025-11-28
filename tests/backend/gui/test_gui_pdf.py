
# tests\backend\gui\test_gui_pdf.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.pdf import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIPdf:
    def test_index(self):
        url = FlaskRoute.get_url(pdf_index)
        Test.flask_webpage(url)

    def test_compress(self):
        url = FlaskRoute.get_url(pdf_compress)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(pdf_convert)
        Test.flask_webpage(url)

    def test_decrypt(self):
        url = FlaskRoute.get_url(pdf_decrypt)
        Test.flask_webpage(url)

    def test_encrypt(self):
        url = FlaskRoute.get_url(pdf_encrypt)
        Test.flask_webpage(url)

    def test_extract_img(self):
        url = FlaskRoute.get_url(pdf_extract_img)
        Test.flask_webpage(url)

    def test_extract(self):
        url = FlaskRoute.get_url(pdf_extract)
        Test.flask_webpage(url)

    def test_merge(self):
        url = FlaskRoute.get_url(pdf_merge)
        Test.flask_webpage(url)

    # DO NOT TEST OCR PAGE, AS IT REQUIRES INTERNET ACCESS TO CHECK AVAILABLE TESSERACT DATASETS (CAN FAIL IN CI/CD)
    # def test_ocr(self):
    #     url = FlaskRoute.get_url(pdf_ocr)
    #     Test.flask_webpage(url)

    def test_repair(self):
        url = FlaskRoute.get_url(pdf_repair)
        Test.flask_webpage(url)

    def test_rotate(self):
        url = FlaskRoute.get_url(pdf_rotate)
        Test.flask_webpage(url)

    def test_split(self):
        url = FlaskRoute.get_url(pdf_split)
        Test.flask_webpage(url)
