
# src\file_conversor\config\locale.py

import gettext  # app translations / locales
import locale

from file_conversor.config.environment import Environment
from file_conversor.config.config import Configuration

CONFIG = Configuration.get_instance()


def normalize_lang_code(lang: str | None):
    if not lang or "_" not in lang:
        print(f"ERROR: invalid language code '{lang}'")
        return None  # empty language code (force fallback in translation)
    return lang


# Get translations
def get_system_locale():
    """Get system default locale"""
    lang, _ = locale.getlocale()
    return lang


def get_translation():
    """
    Get translation mechanism, based on user preferences.
    """
    try:
        languages = [
            normalize_lang_code(CONFIG["language"]),
            normalize_lang_code(get_system_locale()),
            "en_US",  # fallback
        ]
        translation = gettext.translation(
            'messages', Environment.get_locales_folder(),
            languages=[lang for lang in languages if lang],  # Filter out None entries
            fallback=False
        )
    except:
        print("Sys lang:", get_system_locale())
        print("Locales folder:", Environment.get_locales_folder())
        print("Languages tried:", languages)
        raise
    return translation.gettext
