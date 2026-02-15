
# src\file_conversor\config\locale.py
from typing import Callable

from rich import print

from file_conversor.config.config import Configuration
from file_conversor.config.environment import Environment


CONFIG = Configuration.get()

AVAILABLE_LANGUAGES: set[str] = {
    str(mo.relative_to(Environment.get_locales_folder()).parts[0])
    for mo in Environment.get_locales_folder().glob("**/LC_MESSAGES/*.mo")
}

_translation_cache: dict[str, Callable[[str], str]] = {}


def _get_lang_name_babel(lang_code: str) -> str:
    """
    Get language name using babel library.

    :param lang_code: Language code (e.g., "en", "fr", "es", "eng", "en_US")

    :return: Language name (e.g., "English", "Français", "Español")
    :raises Exception: If language code is invalid or name not found.
    """
    from babel import Locale

    locale = Locale.parse(lang_code)
    try:
        display_lang = normalize_lang_code(CONFIG.language)[:2].lower()
        lang = locale.get_display_name(display_lang)
        if not lang:
            raise ValueError(f"No language name found for display language '{display_lang}'.")
    except Exception as e:
        display_lang = get_default_language()[:2].lower()
        lang = locale.get_display_name(display_lang)
        if not lang:
            raise ValueError(f"No language name found for display language '{display_lang}'.") from e
    return lang


def _get_lang_name_pycountry(lang_code: str) -> str:
    """
    Get language name using pycountry library.

    :param lang_code: Language code (e.g., "en", "fr", "es", "eng", "en_US")
    :return: Language name (e.g., "English", "Français", "Español")
    :raises Exception: If language code is invalid or name not found.
    """
    import pycountry

    CUSTOM_LANG_ALIASES = {
        "chi_sim": "Chinese (Simplified)",
        "chi_tra": "Chinese (Traditional)",
        "chi_sim_vert": "Chinese (Simplified, Vertical)",
        "chi_tra_vert": "Chinese (Traditional, Vertical)",
        "equ": "Mathematical Equations (OCR)",
        "osd": "Orientation & Script Detection",
    }

    base_code = lang_code.split('_')[0]  # remove region part like en_US → en
    lang = pycountry.languages.get(alpha_3=base_code)
    if not lang:
        lang = pycountry.languages.get(alpha_2=base_code)
    if lang and hasattr(lang, 'name'):
        return str(lang.name)
    if lang_code in CUSTOM_LANG_ALIASES:
        return CUSTOM_LANG_ALIASES[lang_code]
    raise ValueError(f"No language name found for code '{lang_code}'.")


def _print_debug():
    print(f"Locales folder: {Environment.get_locales_folder()}")
    print(f"Available languages: {sorted(AVAILABLE_LANGUAGES)} ({len(AVAILABLE_LANGUAGES)} entries)")
    print(f"Config / sys lang: ({CONFIG.language} / {get_system_locale()})")


def get_default_language():
    return "en_US"


def normalize_lang_code(lang: str | None) -> str:
    if not lang or lang not in AVAILABLE_LANGUAGES:
        return ""  # empty language code (force fallback in translation)
    return lang


# Get translations
def get_system_locale():
    """Get system default locale"""
    import locale

    lang, _ = locale.getlocale()
    return lang


def get_translation():
    """
    Get translation mechanism, based on user preferences.
    """
    import gettext  # app translations / locales

    if "gettext" in _translation_cache:
        return _translation_cache["gettext"]

    languages: list[str] = []
    try:
        languages = [
            normalize_lang_code(CONFIG.language),
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
        _translation_cache["gettext"] = translation.gettext
        return _translation_cache["gettext"]
    except:
        _print_debug()
        print(f"Languages tried: {languages}")
        raise


def get_language_name(lang_code: str) -> str:
    """
    Get language name from code.

    :param lang_code: Language code (e.g., "en", "fr", "es", "eng", "en_US")

    :return: Language name (e.g., "English", "Français", "Español")
    """
    lang_code = lang_code.strip().replace('-', '_')

    try:
        return _get_lang_name_babel(lang_code).title()
    except Exception:
        """ If babel fails (e.g., due to missing locale data), fallback to pycountry. If that also fails, fallback to the original code. """
    try:
        return _get_lang_name_pycountry(lang_code).title()
    except Exception:
        print(f"[bold]WARNING[/]: Could not parse language code '{lang_code}'. Falling back to '{lang_code}'.")
        return lang_code


__all__ = [
    "AVAILABLE_LANGUAGES",
    "get_default_language",
    "normalize_lang_code",
    "get_system_locale",
    "get_translation",
    "get_language_name",
]
