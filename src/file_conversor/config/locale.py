
# src\config\locale.py

import gettext  # app translations / locales
import locale

from pathlib import Path  # current sys locale

from file_conversor.config.state import State

STATE = State.get_instance()


# Get translations
def get_system_locale():
    """Get system default locale"""
    lang, _ = locale.getlocale()
    return lang


def get_translation(lang: str = ""):
    """
    Get translation mechanism for the language specified.

    :param lang: Language requested by user. Defaults to "" (no user-defined language).
    """
    sys_lang = get_system_locale()
    translation = gettext.translation(
        'messages', State.get_resources_folder() / "locales",
        languages=[
            lang,
            sys_lang if sys_lang else "en_US",
            "en_US",  # fallback
        ],
        fallback=False
    )
    return translation.gettext
