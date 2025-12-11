# src/file_conversor/backend/gui/_api/config.py

from flask import json, render_template, url_for

from typing import Any

# user-provided modules
from file_conversor.backend.gui.flask_api import FlaskApi, FlaskApiStatus

from file_conversor.config import Configuration, ConfigurationData, Environment, Log, State
from file_conversor.config.locale import get_translation

# Get app config
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


def config_thread(params: dict[str, Any], status: FlaskApiStatus) -> None:
    """API endpoint to update the application configuration."""
    logger.info(f"[bold]{_('Configuration update requested via API.')}[/]")
    Configuration.set(ConfigurationData(
        cache_enabled=params['cache-enabled'],
        cache_expire_after=params['cache-expire-after'],
        port=params['port'],
        language=params['language'],
        install_deps=params['install-deps'],
        audio_bitrate=params['audio-bitrate'],
        video_bitrate=params['video-bitrate'],
        video_format=params['video-format'],
        video_encoding_speed=params['video-encoding-speed'],
        video_quality=params['video-quality'],
        image_quality=params['image-quality'],
        image_dpi=params['image-dpi'],
        image_fit=params['image-fit'],
        image_page_size=params['image-page-size'],
        image_resampling=params['image-resampling'],
        pdf_compression=params['pdf-compression'],
        gui_zoom=params['gui-zoom'],
        gui_output_dir=params['gui-output-dir'],
    ))
    Configuration.save()
    logger.debug(f"Configuration updated: {Configuration.get()}")


def api_config():
    """API endpoint to update the application configuration."""
    logger.info(f"[bold]{_('Configuration set requested via API.')}[/]")
    return FlaskApi.execute_response(config_thread)
