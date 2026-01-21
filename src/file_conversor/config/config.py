# src\file_conversor\config\config.py

import locale

from pathlib import Path
from typing import Any
from pydantic import BaseModel

from file_conversor.config.environment import Environment


class ConfigurationData(BaseModel):
    """Configuration data structure"""

    cache_enabled: bool
    """http cache enabled"""
    cache_expire_after: int
    """http cache expiration time in seconds"""
    port: int
    """Default port (flask app)"""
    language: str
    """Default: system language or "en_US" """
    install_deps: bool | None
    """Default: ask user to confirm dependency installation"""
    audio_bitrate: int
    """Default audio bitrate in kbps"""
    video_bitrate: int
    """Default video bitrate in kbps"""
    video_format: str
    """Default video format"""
    video_encoding_speed: str
    """Default video encoding speed"""
    video_quality: str
    """Default video quality"""
    image_quality: int
    """Default image quality 90%"""
    image_dpi: int
    """Default image => PDF dpi"""
    image_fit: str
    """Default image => PDF fit mode"""
    image_page_size: str | None
    """Default image => PDF page size"""
    image_resampling: str
    """Default image resampling algorithm"""
    pdf_compression: str
    """Default PDF compression level"""
    gui_zoom: int
    """Default GUI zoom level"""
    gui_output_dir: str
    """Default output directory"""

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {**self.__dict__}


class Configuration:
    """Application configuration manager."""
    __config_path = Environment.get_data_folder() / ".config.json"
    __data: ConfigurationData | None = None

    @classmethod
    def __load(cls) -> ConfigurationData:
        if cls.__config_path.exists():
            return ConfigurationData.model_validate_json(cls.__config_path.read_text())
        return cls.__reset()

    @classmethod
    def __reset(cls) -> ConfigurationData:
        language = "en_US"
        if locale.getlocale() and locale.getlocale()[0]:
            language = locale.getlocale()[0] or language

        return ConfigurationData(
            cache_enabled=True,     # Enable HTTP cache
            cache_expire_after=int(30 * 24 * 60 * 60),  # HTTP cache expiration time in seconds (30 days)
            port=5000,              # Default port (flask app)
            language=language,      # Default: system language or "en_US"
            install_deps=True,      # Default: ask user to confirm dependency installation
            audio_bitrate=0,        # Default audio bitrate in kbps
            video_bitrate=0,        # Default video bitrate in kbps
            video_format="mp4",     # Default video format
            video_encoding_speed="medium",  # Default video encoding speed
            video_quality="medium",  # Default video quality
            image_quality=90,        # Default image quality 90%
            image_dpi=200,           # Default image => PDF dpi
            image_fit='into',        # Default image => PDF fit mode
            image_page_size=None,    # Default image => PDF page size
            image_resampling="bicubic",  # Default image resampling algorithm
            pdf_compression="medium",  # Default PDF compression level
            gui_zoom=100,            # Default GUI zoom level
            gui_output_dir=str(Environment.UserFolder.DOWNLOADS()),  # Default output directory
        )

    @classmethod
    def set(cls, new_config: ConfigurationData) -> None:
        """Set application configuration data."""
        cls.__data = new_config

    @classmethod
    def get(cls) -> ConfigurationData:
        """Get application configuration data."""
        if cls.__data is None:
            cls.__data = cls.__load()
        return cls.__data

    @classmethod
    def get_path(cls) -> Path:
        """Get configuration file path."""
        return cls.__config_path

    @classmethod
    def save(cls) -> None:
        """Save app configuration file"""
        if cls.__data is None:
            raise RuntimeError("Configuration data is not set.")
        json_str = cls.__data.model_dump_json(indent=2)
        cls.__config_path.write_text(json_str)

    @classmethod
    def load(cls) -> None:
        """Load app configuration file"""
        cls.__data = cls.__load()

    @classmethod
    def reset(cls) -> None:
        """Reset app configuration to factory defaults"""
        cls.__data = cls.__reset()


__all__ = [
    "Configuration",
    "ConfigurationData",
]
