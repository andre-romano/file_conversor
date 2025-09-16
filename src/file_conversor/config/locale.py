
# src\file_conversor\config\locale.py

import gettext  # app translations / locales
import locale

from file_conversor.config.environment import Environment
from file_conversor.config.config import Configuration

CONFIG = Configuration.get_instance()

AVAILABLE_LANGUAGES = set([str(p.name) for p in Environment.get_locales_folder().glob("*") if p.is_dir()])
MO_FILES = ["/".join([mo.parent.parent.name, mo.parent.name, mo.name]) for mo in Environment.get_locales_folder().glob("**/LC_MESSAGES/*.mo")]


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
    languages: list[str] = []
    try:
        languages = [
            normalize_lang_code(CONFIG["language"]),
            normalize_lang_code(get_system_locale()),
            get_default_language(),  # fallback
        ]
        languages = [lang for lang in languages if lang]  # Filter out None entries
        translation = gettext.translation(
            'messages', Environment.get_locales_folder(),
            languages=languages,
            fallback=False,
        )
    except:
        print("Locales folder:", Environment.get_locales_folder())
        print("Available languages:", AVAILABLE_LANGUAGES, f"({len(AVAILABLE_LANGUAGES)} entries)")
        print("Sys lang:", get_system_locale())
        print("Languages tried:", languages, f"({len(languages)} entries)")
        print(".MO Files found:", len(MO_FILES))
        raise
    return translation.gettext
