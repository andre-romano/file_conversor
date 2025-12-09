# tasks_modules\locales.py

import polib
from deep_translator import GoogleTranslator

from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *


def _translate_locale(c: InvokeContext, path: Path):
    exception = None

    locale = path.name
    lang_id = locale.split("_")[0]

    print(f"[bold] Translating locale '{locale}' ... [/]")
    po = polib.pofile(path / "LC_MESSAGES" / "messages.po")

    if not po.untranslated_entries():
        print(f"[bold] Translating locale '{locale}' ... [/][bold yellow]NO CHANGES[/]")
        c.run(f'git checkout "{path}"', hide=True)
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


@task(post=[template])
def backup_i18n(c: InvokeContext):
    """ Backup locales' .PO files"""
    print(f"[bold] Backing up locales .po files ... [/]")
    for path in I18N_PATH.rglob("*.po"):
        po_bak = path.with_suffix(".po.bak")
        shutil.copy2(path, po_bak)
    print(f"[bold] Backing up locales .po files ... [/][bold green]OK[/]")


@task
def recover_i18n(c: InvokeContext):
    """ Recover locales' .PO files from backup"""
    print(f"[bold] Recovering individual locale translations from backup ... [/]")
    for po_bak_path in I18N_PATH.rglob("*.po.bak"):
        po_path = po_bak_path.with_suffix("")

        po = polib.pofile(po_path)
        po_bak = polib.pofile(po_bak_path)

        if not po.untranslated_entries():
            print(f"[bold yellow]WARN:[/] No untranslated entries for '{po_path.parent.parent.name}'. Skipping ... ")
            continue

        print(f"\tRecovering translations for '{po_path.parent.parent}' ... ", end="")
        for entry in po.untranslated_entries():
            bak_entry = po_bak.find(entry.msgid)
            entry.msgstr = bak_entry.msgstr if bak_entry else entry.msgstr
        po.save()
        po_bak_path.unlink()
        print(f"[bold green]OK[/]")
    print(f"[bold] Recovering individual locale translations from backup ... [/][bold green]OK[/]")


@task(pre=[backup_i18n], post=[recover_i18n])
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
    for path in I18N_PATH.glob("*"):
        if not path.is_dir():
            continue
        try:
            _translate_locale(c, path)
        except Exception as e:
            print(f"[bold red] ERROR:[/] {repr(e)}")
            exception = e
    if exception:
        print(f"[bold yellow] WARN:[/] need to rerun [bold white]'locales.update'[/] - {repr(exception)}")
        raise exception

    try:
        c.run(f"git add {I18N_PATH}")
        c.run(f"git commit -m \"locales: automatic translation update\"")
    except:
        print(f"[bold yellow] WARN:[/] nothing to commit in locales")

    print(f"[bold] Translation i18N:[/] [bold green]SUCCESS[/]")


@task
def build(c: InvokeContext):
    """ Build locales' .MO files based on .PO files ..."""
    print(f"[bold] Building locales .mo files ... [/]")
    result = c.run(f"pdm run pybabel compile -d {I18N_PATH}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Building locales .mo files ... [/][bold green]OK[/]")
