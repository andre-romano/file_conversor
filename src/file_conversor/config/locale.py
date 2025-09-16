
# src\file_conversor\config\locale.py

import gettext  # app translations / locales
import locale

from typing import Callable

from file_conversor.config.environment import Environment
from file_conversor.config.config import Configuration

CONFIG = Configuration.get_instance()

AVAILABLE_LANGUAGES = set([str(mo.relative_to(Environment.get_locales_folder()).parts[0]) for mo in Environment.get_locales_folder().glob("**/LC_MESSAGES/*.mo")])

_gettext_instance: Callable[[str], str] | None = None


def _print_debug():
    print(f"Locales folder: {Environment.get_locales_folder()}")
    print(f"Available languages: {sorted(AVAILABLE_LANGUAGES)} ({len(AVAILABLE_LANGUAGES)} entries)")
    print(f"Config / sys lang: ({CONFIG['language']} / {get_system_locale()})")


def get_default_language():
    return "en_US"


def normalize_lang_code(lang: str | None) -> str:
    if not lang or lang not in AVAILABLE_LANGUAGES:
        return ""  # empty language code (force fallback in translation)
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
    global _gettext_instance
    if _gettext_instance:
        return _gettext_instance

    languages: list[str] = []
    try:
        languages = [
            normalize_lang_code(CONFIG["language"]),
            normalize_lang_code(get_system_locale()),
            normalize_lang_code(get_default_language()),  # fallback
        ]
        languages = [lang for lang in languages if lang]  # Filter out None entries
        if not languages:
            print(f"WARNING: No valid languages found")
            _print_debug()
        translation = gettext.translation(
            'messages', Environment.get_locales_folder(),
            languages=languages,
            fallback=True,
        )
        _gettext_instance = translation.gettext
        return _gettext_instance
    except:
        _print_debug()
        print(f"Languages tried: {languages}")
        raise
