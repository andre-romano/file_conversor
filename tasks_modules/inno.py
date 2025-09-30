# tasks_modules\inno.py

import os

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import choco, base, zip

INNO_PATH = Path("inno")
INNO_ISS = INNO_PATH / "setup.iss"

INSTALL_PATH = (Path(os.environ.get('ProgramFiles(x86)') or "") / PROJECT_NAME).resolve()

INNO_APP_EXE = Path(zip.APP_EXE.name)


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        f"{INNO_PATH}",
        "dist",
    ])


@task(pre=[mkdirs])
def clean_inno(c: InvokeContext):
    _config.remove_path(f"{INNO_PATH}/*")


@task(pre=[mkdirs])
def clean_exe(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP_WIN_EXE}")


@task(pre=[clean_inno, zip.check])
def create_manifest(c: InvokeContext):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    if not zip.BUILD_DIR.exists():
        raise RuntimeError(f"Path {zip.BUILD_DIR} does not exist")

    # setup.iss
    setup_iss_path = Path(f"{INNO_ISS}")
    setup_iss_path.write_text(rf'''
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={PROJECT_TITLE}
AppVersion={PROJECT_VERSION}
DefaultDirName={{autopf}}/{PROJECT_NAME}
Compression=LZMA2
ShowLanguageDialog=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SetupIconFile={ICON_APP.resolve()}
UninstallDisplayIcon={{app}}\{ICON_APP.parent.parent.name}\{ICON_APP.parent.name}\{ICON_APP.name}
SourceDir={Path(".").resolve()}
OutputDir={INSTALL_APP_WIN_EXE.parent.resolve()}
OutputBaseFilename={INSTALL_APP_WIN_EXE.with_suffix("").name}
AlwaysRestart=yes

[Files]
Source: "{zip.BUILD_DIR.resolve()}\*"; DestDir: "{{app}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: "{SCRIPTS_PATH.resolve()}\*"; DestDir: "{{tmp}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles

[Registry]
; Adds app_folder to the USER PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: not IsAdmin()

; Adds app_folder to the SYSTEM PATH (requires admin privileges)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: IsAdmin()

[Run]
StatusMsg: "Installing Python ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{tmp}}/{INSTALL_PYTHON.name}"""; WorkingDir: "{{tmp}}"; Flags: runhidden runascurrentuser waituntilterminated
StatusMsg: "Installing {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE}"" win install-menu"""; WorkingDir: "{{src}}"; Flags: runhidden runascurrentuser waituntilterminated

[UninstallRun]
StatusMsg: "Uninstalling {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE}"" win uninstall-menu"""; WorkingDir: "{{src}}"; Flags: runhidden runascurrentuser waituntilterminated
StatusMsg: "Clean up files ..."; Filename: "cmd.exe"; Parameters: "/C rmdir /s /q ""{{app}}"""; Flags: runhidden runascurrentuser

''', encoding="utf-8")
    assert setup_iss_path.exists()
    print("[bold green]OK[/]")

    print(f"{setup_iss_path}:")
    print(setup_iss_path.read_text())


@task(pre=[choco.install])
def install(c: InvokeContext):
    if shutil.which("iscc"):
        return
    print("[bold] Installing InnoSetup ... [/]")
    result = c.run(f'powershell.exe -ExecutionPolicy Bypass -Command "choco install -y innosetup"')
    assert (result is not None) and (result.return_code == 0)
    if not shutil.which("iscc"):
        raise RuntimeError("'iscc' not found in PATH")


@task(pre=[clean_exe, create_manifest, install,], post=[zip.clean_build])
def build(c: InvokeContext):
    print(f"[bold] Building Installer (EXE) ... [/]")
    result = c.run(f"iscc /Qp \"{INNO_ISS}\"")
    assert (result is not None) and (result.return_code == 0)
    if not INSTALL_APP_WIN_EXE.exists():
        raise RuntimeError(f"'{INSTALL_APP_WIN_EXE}' not found")
    print(f"[bold] Building Installer (EXE) ... [/][bold green]OK[/]")


@task(pre=[build,],)
def install_app(c: InvokeContext):
    print(rf'[bold] Installing {PROJECT_NAME} via Inno .EXE ... [/]')
    cmd = [
        rf'"{INSTALL_APP_WIN_EXE}"',
        rf'/DIR="{INSTALL_PATH}"',
        "/SUPPRESSMSGBOXES",
        "/VERYSILENT",
        "/NORESTART",
        "/SP-",
    ]
    result = c.run(" ".join(cmd))
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Installing {PROJECT_NAME} via Inno .EXE ... [/][bold green]OK[/]')


@task
def uninstall_app(c: InvokeContext):
    print(rf'[bold] Uninstalling {PROJECT_NAME} via Inno .EXE ... [/]')
    exe_path = INSTALL_PATH / UNINSTALL_APP_WIN.name
    if not exe_path.exists():
        raise RuntimeError(f"'{exe_path}' not found")
    print(f"[bold]Found uninstaller: '{exe_path}'[/]")
    cmd = [
        rf'"{exe_path}"',
        "/SUPPRESSMSGBOXES",
        "/VERYSILENT",
        "/NORESTART",
        "/SP-",
    ]
    result = c.run(" ".join(cmd))
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Uninstalling {PROJECT_NAME} via Inno .EXE ... [/][bold green]OK[/]')


@task(pre=[install_app,], post=[uninstall_app,])
def check(c: InvokeContext):
    base.check(c, exe=INSTALL_PATH / f"{INNO_APP_EXE}")
