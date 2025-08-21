# tasks_modules\inno.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import pyinstaller, choco, base

INNO_PATH = str("inno")
INNO_ISS = Path(f"{INNO_PATH}/setup.iss")


def get_uninstaller_path() -> Path | None:
    import winreg

    # Registry hives and paths to search
    registry_locations = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]

    for hive, path in registry_locations:
        with winreg.OpenKey(hive, path) as uninstall_key:
            for i in range(winreg.QueryInfoKey(uninstall_key)[0]):
                subkey_name = winreg.EnumKey(uninstall_key, i)
                with winreg.OpenKey(uninstall_key, subkey_name) as subkey:
                    try:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        if PROJECT_TITLE.lower() in display_name.lower():
                            uninstall_str, _ = winreg.QueryValueEx(subkey, "UninstallString")

                            # Some uninstall strings are quoted and have extra args — clean them up
                            if uninstall_str.startswith('"'):
                                exe_path = uninstall_str.split('"')[1]
                            else:
                                exe_path = uninstall_str.split(" ")[0]
                            return exe_path
                    except:
                        pass
    return None


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        INNO_PATH,
        "dist",
    ])


@task(pre=[mkdirs])
def clean_inno(c: InvokeContext):
    _config.remove_path(f"{INNO_PATH}/*")


@task(pre=[mkdirs])
def clean_exe(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP}")


@task(pre=[clean_inno, pyinstaller.check])
def create_manifest(c: InvokeContext):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    APP_DIST_PATH = Path(f"./dist/{PROJECT_NAME}").resolve()
    if not APP_DIST_PATH.exists():
        raise RuntimeError(f"Path {APP_DIST_PATH} does not exist")

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
UninstallDisplayIcon={{app}}\{PROJECT_NAME}.exe
SourceDir={Path(".").resolve()}
OutputDir={Path("./dist").resolve()}
OutputBaseFilename={INSTALL_APP.with_suffix("").name}
AlwaysRestart=yes

[Files]
Source: "{APP_DIST_PATH}\*"; DestDir: "{{app}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 

[Registry]
; Adds app_folder to the USER PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: not IsAdmin()

; Adds app_folder to the SYSTEM PATH (requires admin privileges)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: IsAdmin()

[Run]
StatusMsg: "Installing {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{PROJECT_NAME}.exe"" win install-menu"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated

[UninstallRun]
StatusMsg: "Uninstalling {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{PROJECT_NAME}.exe"" win uninstall-menu"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated
''', encoding="utf-8")
    assert setup_iss_path.exists()
    print("[bold green]OK[/]")


@task(pre=[choco.install])
def install(c: InvokeContext):
    if shutil.which("iscc"):
        return
    print("[bold] Installing InnoSetup ... [/]")
    result = c.run(f'powershell.exe -ExecutionPolicy Bypass -Command "choco install -y innosetup"')
    assert (result is not None) and (result.return_code == 0)
    if not shutil.which("iscc"):
        raise RuntimeError("'iscc' not found in PATH")


@task
def gen_hash(c: InvokeContext):
    print(f"[bold] Generating SHA256 hash ... [/]")
    if not INSTALL_APP.exists():
        raise RuntimeError(f"File {INSTALL_APP} not found")
    hash = _config.get_hash(INSTALL_APP)
    INSTALL_APP_HASH.write_text(rf"""
{hash}  {INSTALL_APP.name}
""", encoding="utf-8")
    if not INSTALL_APP_HASH.exists():
        raise RuntimeError("Failed to create sha256 file")
    print(f"[bold] Generating SHA256 hash ... [/][bold green]OK[/]")


@task(pre=[clean_exe, create_manifest, install,], post=[gen_hash])
def build(c: InvokeContext):
    print(f"[bold] Building Installer (EXE) ... [/]")
    result = c.run(f"iscc /Qp \"{INNO_ISS}\"")
    assert (result is not None) and (result.return_code == 0)
    if not list(Path("dist").glob("*.exe")):
        raise RuntimeError("Build EXE - Empty dist/*.exe")
    print(f"[bold] Building Installer (EXE) ... [/][bold green]OK[/]")


@task(pre=[build,],)
def install_app(c: InvokeContext):
    print(rf'[bold] Installing {PROJECT_NAME} via Inno .EXE ... [/]')
    exe_path = list(Path("dist").glob("*.exe"))[0]
    result = c.run(rf'"{exe_path}" /SUPPRESSMSGBOXES /VERYSILENT /NORESTART')
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Installing {PROJECT_NAME} via Inno .EXE ... [/][bold green]OK[/]')


@task
def uninstall_app(c: InvokeContext):
    print(rf'[bold] Uninstalling {PROJECT_NAME} via Inno .EXE ... [/]')
    exe_path = get_uninstaller_path()
    if not exe_path:
        raise RuntimeError(f"Uninstaller for '{PROJECT_TITLE}' not found")
    print(f"[bold]Found uninstaller: '{exe_path}'[/]")
    result = c.run(rf'"{exe_path}" /SUPPRESSMSGBOXES /VERYSILENT /NORESTART')
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Uninstalling {PROJECT_NAME} via Inno .EXE ... [/][bold green]OK[/]')


@task(pre=[install_app,], post=[uninstall_app,])
def check(c: InvokeContext):
    base.check(c)
