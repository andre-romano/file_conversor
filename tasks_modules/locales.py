# tasks_modules\locales.py

import polib
from deep_translator import GoogleTranslator

from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *


def _translate_locale(path: Path):
    exception = None

    locale = path.name
    lang_id = locale.split("_")[0]

    print(f"[bold] Translating locale '{locale}' ... [/]")
    po = polib.pofile(path / "LC_MESSAGES" / "messages.po")

    if not po.untranslated_entries():
        print(f"[bold] Translating locale '{locale}' ... [/][bold yellow]NO CHANGES[/]")
        return

    translator = GoogleTranslator(source="en", target=lang_id)
    for entry in po.untranslated_entries():
        try:
            print(f"\tTranslating '{lang_id}/{entry.msgid}' ... ", end="")
            entry.msgstr = entry.msgid if locale == "en_US" else translator.translate(entry.msgid)
            print(f"[bold green]OK[/]")
        except Exception as e:
            print(f"[bold red]FAILED[/]")
            exception = e
    po.save()

    if exception:
        print(f"[bold] Translating locale '{locale}' ... [/][bold red]FAILED[/]")
        raise exception
    print(f"[bold] Translating locale '{locale}' ... [/][bold green]OK[/]")


@task
def template(c: InvokeContext):
    """ Update locales template (.pot)"""
    print(f"[bold] Creating locales template (.pot) ... [/]", end="")
    result = c.run(f"pdm run pybabel extract -F babel.cfg -o {I18N_TEMPLATE} .")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Creating locales template (.pot) ... [/][bold green]OK[/]")


@task(pre=[template])
def create(c, locale: str):
    """
    Create a locale (e.g., en_US, pt_BR, etc) translation using Babel.

    :param locale: Locale code (e.g., en_US, pt_BR, etc)
    """
    print(f"[bold] Creating new locale '{locale}' ... [/]")
    result = c.run(f"pdm run pybabel init -i {I18N_TEMPLATE} -d {I18N_PATH} -l {locale}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Creating new locale '{locale}' ... [/][bold green]OK[/]")


@task(pre=[template])
def update(c: InvokeContext):
    """ Update locales' .PO files based on current template (.pot)"""
    print(f"[bold] Updating locales based on template .pot file ... [/]")
    result = c.run(f"pdm run pybabel update -i {I18N_TEMPLATE} -d {I18N_PATH} --no-fuzzy-matching")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Updating locales based on template .pot file ... [/][bold green]OK[/]")


@task(pre=[update])
def translate(c: InvokeContext):
    """ Translate locales' .PO files using Google Translate"""
    exception = None
    for path in Path(I18N_PATH).glob("*"):
        if not path.is_dir():
            continue
        try:
            _translate_locale(path)
        except Exception as e:
            print(f"[bold red] ERROR:[/] {repr(e)}")
            exception = e
    if exception:
        print(f"[bold yellow] WARN:[/] need to rerun [bold white]'locales.update'[/] - {repr(exception)}")
        raise exception
    print(f"[bold] Translation i18N:[/] [bold green]SUCCESS[/]")


@task
def build(c: InvokeContext):
    """ Build locales' .MO files based on .PO files ..."""
    print(f"[bold] Building locales .mo files ... [/]")
    result = c.run(f"pdm run pybabel compile -d {I18N_PATH}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Building locales .mo files ... [/][bold green]OK[/]")
