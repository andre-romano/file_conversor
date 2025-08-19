
# src\file_conversor\config\locale.py

import gettext  # app translations / locales
import locale

from file_conversor.config.environment import Environment
from file_conversor.config.config import Configuration

CONFIG = Configuration.get_instance()


# Get translations
def get_system_locale():
    """Get system default locale"""
    lang, _ = locale.getlocale()
    return lang


def get_translation():
    """
    Get translation mechanism, based on user preferences.
    """
    sys_lang = get_system_locale()
    translation = gettext.translation(
        'messages', Environment.get_locales_folder(),
        languages=[
            CONFIG["language"],
            sys_lang if sys_lang else "en_US",
            "en_US",  # fallback
        ],
        fallback=False
    )
    return translation.gettext
