# tasks_modules\inno.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import choco, base

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
    _config.remove_path(f"dist/*.exe")


@task(pre=[clean_inno,])
def create_manifest(c: InvokeContext):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    if not INSTALL_SCOOP.exists():
        raise RuntimeError(f"File {INSTALL_SCOOP} does not exist")

    install_ps1_path = Path(f"{INNO_PATH}/install.ps1")
    install_ps1_path.write_text(rf'''
$ErrorActionPreference = 'Stop'
$log_file = "{PROJECT_NAME}-install.log"

Write-Output "Add {PROJECT_NAME} bucket ..."
& scoop bucket add "{PROJECT_NAME}" "{PROJECT_HOMEPAGE}" | Tee-Object -FilePath "$log_file"

Write-Output "Installing {PROJECT_NAME} ..."
& scoop install "{PROJECT_NAME}@{PROJECT_VERSION}" -s -k @args | Tee-Object -FilePath "$log_file" -Append

if (-not (Get-Command "{PROJECT_NAME}" -ErrorAction SilentlyContinue)) {{
    Write-Error "'{PROJECT_NAME}' not found in PATH" | Tee-Object -FilePath "$log_file" -Append
    exit 1
}}
''', encoding='utf-8')
    assert install_ps1_path.exists()

    uninstall_ps1_path = Path(f"{INNO_PATH}/uninstall.ps1")
    uninstall_ps1_path.write_text(rf'''
$ErrorActionPreference = 'Stop'
$log_file = "{PROJECT_NAME}-uninstall.log"

Write-Output "Uninstalling {PROJECT_NAME} ..."
& scoop uninstall "{PROJECT_NAME}" @args | Tee-Object -FilePath "$log_file"

Write-Output "Remove {PROJECT_NAME} bucket ..."
& scoop bucket rm "{PROJECT_NAME}" | Tee-Object -FilePath "$log_file" -Append

if (Get-Command "{PROJECT_NAME}" -ErrorAction SilentlyContinue) {{
    Write-Error "'{PROJECT_NAME}' STILL installed in PATH" | Tee-Object -FilePath "$log_file" -Append
    exit 1
}}
''', encoding='utf-8')
    assert uninstall_ps1_path.exists()

    # setup.iss
    setup_iss_path = Path(f"{INNO_ISS}")
    setup_iss_path.write_text(rf'''
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={PROJECT_TITLE}
AppVersion={PROJECT_VERSION}
DefaultDirName={{autopf}}/{PROJECT_TITLE}
DisableDirPage=yes
Compression=LZMA2
ShowLanguageDialog=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SourceDir={Path(".").resolve()}
OutputDir={Path("./dist").resolve()}
OutputBaseFilename={PROJECT_NAME}-{GIT_RELEASE}-Win_x64-Installer

[Files]
Source: "{Path(SCRIPTS_PATH).resolve()}\*"; DestDir: "{{app}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 
Source: "{Path(install_ps1_path).resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 
Source: "{Path(uninstall_ps1_path).resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 

[Run]
StatusMsg: "Installing Scoop ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{app}}\{INSTALL_SCOOP.name}"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated
StatusMsg: "Installing {PROJECT_NAME} (for ALL USERS) ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{app}}\{install_ps1_path.name}"" ""-g"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated; Check: IsAdmin
StatusMsg: "Installing {PROJECT_NAME} (for current user) ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{app}}\{install_ps1_path.name}"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated; Check: not IsAdmin

[UninstallRun]
StatusMsg: "Uninstalling {PROJECT_NAME} (for ALL USERS) ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{app}}\{uninstall_ps1_path.name}"" ""-g"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated; Check: IsAdmin
StatusMsg: "Uninstalling {PROJECT_NAME} (for current user) ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{app}}\{uninstall_ps1_path.name}"""; WorkingDir: "{{src}}"; Flags: runascurrentuser waituntilterminated; Check: not IsAdmin

[Code]
function IsAdmin: Boolean;
begin
  Result := IsAdminLoggedOn;
end;
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


@task(pre=[clean_exe, create_manifest, install,])
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
