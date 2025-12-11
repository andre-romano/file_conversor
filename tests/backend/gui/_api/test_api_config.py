# tests\backend\gui\_api\test_api_config.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.gui.flask_api_status import *

from file_conversor.config.config import Configuration

from tests.utils import Test, DATA_PATH, app_cmd

CONFIG = Configuration.get()


class TestAPIConfig:
    route = "/api/config"

    def test_config(self):
        reply = Test.flask_api(self.route, data={
            'cache-enabled': CONFIG.cache_enabled,
            'cache-expire-after': CONFIG.cache_expire_after,
            'port': CONFIG.port,
            'language': CONFIG.language,
            'install-deps': CONFIG.install_deps,
            'audio-bitrate': CONFIG.audio_bitrate,
            'video-bitrate': CONFIG.video_bitrate,
            'video-format': CONFIG.video_format,
            'video-encoding-speed': CONFIG.video_encoding_speed,
            'video-quality': CONFIG.video_quality,
            'image-quality': CONFIG.image_quality,
            'image-dpi': CONFIG.image_dpi,
            'image-fit': CONFIG.image_fit,
            'image-page-size': CONFIG.image_page_size,
            'image-resampling': CONFIG.image_resampling,
            'pdf-compression': CONFIG.pdf_compression,
            'gui-zoom': CONFIG.gui_zoom,
            'gui-output-dir': CONFIG.gui_output_dir,
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
