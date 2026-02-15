# src\file_conversor\config\config.py

import locale

from pathlib import Path
from typing import Any

from pydantic import BaseModel

from file_conversor.config.environment import Environment


class ConfigurationData(BaseModel):
    """Configuration data structure"""

    cache_enabled: bool = True     # Enable HTTP cache
    """http cache enabled"""
    cache_expire_after: int = int(30 * 24 * 60 * 60)  # HTTP cache expiration time in seconds (30 days)
    """http cache expiration time in seconds"""
    api_port: int = 5000              # Default port (flask app)
    """Default port (flask app)"""
    language: str
    """Default: system language or "en_US" """
    install_deps: bool | None = True      # Default: ask user to confirm dependency installation
    """Default: ask user to confirm dependency installation"""
    audio_bitrate: int | None = None        # Default audio bitrate in kbps
    """Default audio bitrate in kbps"""
    video_bitrate: int | None = None        # Default video bitrate in kbps
    """Default video bitrate in kbps"""
    audio_format: str = "mp3"     # Default audio format
    """Default audio format"""
    video_format: str = "mp4"     # Default video format
    """Default video format"""
    video_profile: str = "medium"  # Default video profile
    """Default video profile"""
    video_encoding_speed: str = "medium"  # Default video encoding speed
    """Default video encoding speed"""
    video_quality: str = "medium"  # Default video quality
    """Default video quality"""
    image_quality: int = 90        # Default image quality 90%
    """Default image quality 90%"""
    image_dpi: int = 200           # Default image => PDF dpi
    """Default image => PDF dpi"""
    image_fit: str = "into"        # Default image => PDF fit mode
    """Default image => PDF fit mode"""
    image_page_size: str = "none"    # Default image => PDF page size
    """Default image => PDF page size"""
    image_resampling: str = "bicubic"  # Default image resampling algorithm
    """Default image resampling algorithm"""
    pdf_compression: str = "medium"  # Default PDF compression level
    """Default PDF compression level"""
    gui_zoom: int = 100            # Default GUI zoom level
    """Default GUI zoom level"""
    gui_output_dir: str = str(Environment.UserFolder.downloads())  # Default output directory
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
        match locale.getlocale():
            case (None, _):
                language = "en_US"
            case (lang, _):
                language = lang
        return ConfigurationData(language=language)

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
