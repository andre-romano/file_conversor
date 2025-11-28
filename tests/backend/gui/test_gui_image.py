
# tests\backend\gui\test_gui_image.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.image import *
from file_conversor.backend.gui.flask_route import FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


class TestGUIImage:
    def test_index(self):
        url = FlaskRoute.get_url(image_index)
        Test.flask_webpage(url)

    def test_antialias(self):
        url = FlaskRoute.get_url(image_antialias)
        Test.flask_webpage(url)

    def test_blur(self):
        url = FlaskRoute.get_url(image_blur)
        Test.flask_webpage(url)

    def test_compress(self):
        url = FlaskRoute.get_url(image_compress)
        Test.flask_webpage(url)

    def test_convert(self):
        url = FlaskRoute.get_url(image_convert)
        Test.flask_webpage(url)

    def test_enhance(self):
        url = FlaskRoute.get_url(image_enhance)
        Test.flask_webpage(url)

    def test_filter(self):
        url = FlaskRoute.get_url(image_filter)
        Test.flask_webpage(url)

    def test_info(self):
        url = FlaskRoute.get_url(image_info)
        Test.flask_webpage(url)

    def test_mirror(self):
        url = FlaskRoute.get_url(image_mirror)
        Test.flask_webpage(url)

    def test_render(self):
        url = FlaskRoute.get_url(image_render)
        Test.flask_webpage(url)

    def test_resize(self):
        url = FlaskRoute.get_url(image_resize)
        Test.flask_webpage(url)

    def test_rotate(self):
        url = FlaskRoute.get_url(image_rotate)
        Test.flask_webpage(url)

    def test_to_pdf(self):
        url = FlaskRoute.get_url(image_to_pdf)
        Test.flask_webpage(url)

    def test_unsharp(self):
        url = FlaskRoute.get_url(image_unsharp)
        Test.flask_webpage(url)
