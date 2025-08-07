# tasks_modules\inno.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import choco

INNO_PATH = str(PYPROJECT["tool"]["myproject"]["inno_path"])
INNO_ISS = Path(f"{INNO_PATH}/setup.iss")


@task
def mkdirs(c):
    _config.mkdir([
        INNO_PATH,
        "dist",
    ])


@task(pre=[mkdirs])
def clean_inno(c):
    _config.remove_path(f"{INNO_PATH}/*")


@task(pre=[mkdirs])
def clean_exe(c):
    _config.remove_path(f"dist/*.exe")


@task(pre=[clean_inno,])
def create_manifest(c):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    if not INSTALL_CHOCO.exists():
        raise RuntimeError(f"Create Inno Files - Script {INSTALL_CHOCO} does not exist")

    # chocolateyInstall.ps1
    setup_path = Path(f"{INNO_ISS}")
    setup_path.write_text(rf'''
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={PROJECT_NAME}
AppVersion={PROJECT_VERSION}
DefaultDirName={{tmp}}  
DisableWelcomePage=yes  
DisableDirPage=yes
DisableReadyPage=yes  
DisableFinishedPage=yes 
DisableProgramGroupPage=yes 
DisableReadyMemo=yes 
DisableStartupPrompt=yes
Compression=LZMA2
ShowLanguageDialog=yes
PrivilegesRequired=admin
SourceDir={Path(".").resolve()}
OutputDir={Path("./dist").resolve()}
OutputBaseFilename={PROJECT_NAME}-{GIT_RELEASE}-Win_x64-Installer

[Files]
Source: "{INSTALL_CHOCO.resolve()}"; DestDir: "{{tmp}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 

[Run]
; Install chocolatey
StatusMsg: "Installing Chocolatey ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{tmp}}\{INSTALL_CHOCO.name}"""; Flags: runascurrentuser waituntilterminated
StatusMsg: "Installing App ..." ; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""choco install {PROJECT_NAME} --version {PROJECT_VERSION} -y"""; Flags: runascurrentuser waituntilterminated
''', encoding="utf-8")
    print("[bold green]OK[/]")


@task(pre=[choco.install])
def install(c):
    if shutil.which("iscc"):
        return
    print("[bold] Installing InnoSetup ... [/]")
    c.run(f'powershell.exe -ExecutionPolicy Bypass -Command "choco install -y innosetup"')
    if not shutil.which("iscc"):
        raise RuntimeError("'iscc' not found in PATH")


@task(pre=[clean_exe, create_manifest, install,])
def build(c):
    print(f"[bold] Building Installer (EXE) ... [/]")
    c.run(f"iscc /Qp \"{INNO_ISS}\"")
    if not list(Path("dist").glob("*.exe")):
        raise RuntimeError("Build EXE - Empty dist/*.exe")
    print(f"[bold] Building Installer (EXE) ... [/][bold green]OK[/]")
