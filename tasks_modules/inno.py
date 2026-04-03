# tasks_modules\inno.py


from pathlib import Path

from invoke.tasks import task  # pyright: ignore[reportUnknownVariableType]

# user provided
from tasks_modules import _config, base, choco, pyapp
from tasks_modules._config import *  # noqa: S2208


INNO_PATH = Path("inno")
INNO_ISS = (INNO_PATH / "setup.iss").resolve()

INSTALL_PATH = (Path("build") / PROJECT_NAME).resolve()

INNO_APP_EXE = pyapp.PORTABLE_EXE
INNO_APP_GUI_EXE = pyapp.PORTABLE_GUI_EXE

build_exe = pyapp.check


@task
def mkdirs(_: InvokeContext):
    _config.mkdir([
        f"{INNO_PATH}",
        "dist",
    ])


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_inno(_: InvokeContext):
    _config.remove_path_pattern(f"{INNO_PATH}/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_exe(_: InvokeContext):
    _config.remove_path_pattern(f"{INSTALL_APP_WIN_EXE}")


@task(pre=[clean_inno, build_exe])  # pyright: ignore[reportUntypedFunctionDecorator]
def create_manifest(_: InvokeContext):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    APP_ICON_RELATIVE_DIR = rf"{{app}}\{ICON_APP.name}"

    # setup.iss
    INNO_ISS.write_text(rf'''
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={PROJECT_TITLE}
AppVersion={PROJECT_VERSION}
DefaultDirName={{autopf}}/{PROJECT_NAME}
Compression=lzma2/max
SolidCompression=yes
ShowLanguageDialog=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
LicenseFile={LICENSE_PATH.resolve()}
InfoBeforeFile={NOTICE_PATH.resolve()}
SetupIconFile={ICON_APP.resolve()}
UninstallDisplayIcon={APP_ICON_RELATIVE_DIR}
SourceDir={Path(".").resolve()}
OutputDir={INSTALL_APP_WIN_EXE.parent.resolve()}
OutputBaseFilename={INSTALL_APP_WIN_EXE.with_suffix("").name}

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Types]
Name: "{InnoTypes.FULL}"; Description: "Full installation"
Name: "{InnoTypes.COMPACT}"; Description: "Compact installation"
Name: "{InnoTypes.CUSTOM}"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: {InnoComponents.CLI}; Description: Command-line interface (CLI); Types: {InnoTypes.FULL} {InnoTypes.COMPACT}; ExtraDiskSpaceRequired: {InnoComponents.CLI.get_space()}
Name: {InnoComponents.GUI}; Description: Graphical user interface (GUI); Types: {InnoTypes.FULL}; ExtraDiskSpaceRequired: {InnoComponents.GUI.get_space()}

[Tasks]
Name: {InnoTasks.DESKTOP_ICON}; Description: Create desktop icon; Components: {InnoComponents.GUI}
Name: {InnoTasks.START_MENU_ICON}; Description: Create start menu icon; Components: {InnoComponents.GUI}
Name: {InnoTasks.CTX_MENU}; Description: Install context menu entries; Components: {InnoComponents.CLI}; Flags: restart

[Dirs]
Name: "{{app}}"; Permissions: everyone-full

[Files]
Source: "{INNO_APP_EXE.resolve()}"; DestDir: "{{app}}"; Components: {InnoComponents.CLI}; Flags: ignoreversion allowunsafefiles
Source: "{INNO_APP_GUI_EXE.resolve()}"; DestDir: "{{app}}"; Components: {InnoComponents.GUI}; Flags: ignoreversion allowunsafefiles
Source: "{LICENSE_PATH.resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion allowunsafefiles
Source: "{NOTICE_PATH.resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion allowunsafefiles
Source: "{THIRD_PARTY_LICENSES_PATH.resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion allowunsafefiles
Source: "{ICON_APP.resolve()}"; DestDir: "{{app}}"; Flags: ignoreversion allowunsafefiles

[Registry]
; Adds app_folder to the USER PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: not IsAdmin()

; Adds app_folder to the SYSTEM PATH (requires admin privileges)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{{olddata}};{{app}}"; Flags: preservestringtype; Check: IsAdmin()

[Icons]
Name: "{{group}}\File Conversor"; Filename: "{{app}}\{INNO_APP_GUI_EXE.name}"; WorkingDir: "{{app}}"; IconFilename: "{APP_ICON_RELATIVE_DIR}"; Tasks: {InnoTasks.START_MENU_ICON}
Name: "{{autodesktop}}\File Conversor"; Filename: "{{app}}\{INNO_APP_GUI_EXE.name}"; WorkingDir: "{{app}}"; IconFilename: "{APP_ICON_RELATIVE_DIR}"; Tasks: {InnoTasks.DESKTOP_ICON}

[Run]
StatusMsg: "Installing Python dependencies using CLI (this might take a while) ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE.name}"" -V"""; WorkingDir: "{{app}}"; Components: {InnoComponents.CLI}; Flags: runhidden runascurrentuser waituntilterminated
StatusMsg: "Installing Python dependencies using GUI (this might take a while) ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_GUI_EXE.name}"" -V"""; WorkingDir: "{{app}}"; Components: {InnoComponents.GUI}; Flags: runhidden runascurrentuser waituntilterminated
StatusMsg: "Installing {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE.name}"" win install-menu"""; WorkingDir: "{{app}}"; Tasks: {InnoTasks.CTX_MENU}; Flags: runhidden runascurrentuser waituntilterminated

[UninstallRun]
StatusMsg: "Uninstalling {PROJECT_NAME} context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE.name}"" win uninstall-menu"""; WorkingDir: "{{app}}"; Tasks: {InnoTasks.CTX_MENU}; Flags: runhidden runascurrentuser waituntilterminated; RunOnceId: "uninstall_menu"
StatusMsg: "Uninstalling {PROJECT_NAME} dependencies for CLI ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_EXE.name}"" self remove"""; WorkingDir: "{{app}}"; Components: {InnoComponents.CLI}; Flags: runhidden runascurrentuser waituntilterminated; RunOnceId: "cli_dependencies_cleanup"
StatusMsg: "Uninstalling {PROJECT_NAME} dependencies for GUI ..."; Filename: "cmd.exe"; Parameters: "/C """"{{app}}\{INNO_APP_GUI_EXE.name}"" self remove"""; WorkingDir: "{{app}}"; Components: {InnoComponents.GUI}; Flags: runhidden runascurrentuser waituntilterminated; RunOnceId: "gui_dependencies_cleanup"
StatusMsg: "Clean up files ..."; Filename: "cmd.exe"; Parameters: "/C rmdir /s /q ""{{app}}"""; Flags: runhidden runascurrentuser; RunOnceId: "cleanup_files"

''', encoding="utf-8")
    assert INNO_ISS.exists()
    print("[bold green]OK[/]")

    print(f"{INNO_ISS}:")
    print(INNO_ISS.read_text())


@task(pre=[choco.install])  # pyright: ignore[reportUntypedFunctionDecorator, reportUnknownMemberType]
def install(c: InvokeContext):
    if shutil.which(cmd="iscc"):
        return
    print("[bold] Installing InnoSetup ... [/]")
    result = c.run(f'powershell.exe -ExecutionPolicy Bypass -Command "choco install -y innosetup"')
    assert (result is not None) and (result.return_code == 0)
    if not shutil.which(cmd="iscc"):
        raise RuntimeError("'iscc' not found in PATH")


@task(pre=[clean_exe, create_manifest, install,])  # pyright: ignore[reportUntypedFunctionDecorator]
def build(c: InvokeContext):
    print(f"[bold] Building Installer (EXE) ... [/]")
    result = c.run(f"iscc /Qp \"{INNO_ISS}\"")
    assert (result is not None) and (result.return_code == 0)
    if not INSTALL_APP_WIN_EXE.exists():
        raise RuntimeError(f"'{INSTALL_APP_WIN_EXE}' not found")
    print(f"[bold] Building Installer (EXE) ... [/][bold green]OK[/]")


@task(pre=[build,],)  # pyright: ignore[reportUntypedFunctionDecorator]
def install_app(c: InvokeContext):
    print(rf'[bold] Installing {PROJECT_NAME} via Inno .EXE ... [/]')
    _config.remove_path_pattern(str(INSTALL_PATH))
    INSTALL_PATH.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        rf'"{INSTALL_APP_WIN_EXE}"',
        rf"/TYPE=${InnoTypes.FULL}",
        rf'/DIR="{INSTALL_PATH}"',
        "/CURRENTUSER",
        "/SUPPRESSMSGBOXES",
        "/VERYSILENT",
        "/NORESTART",
        "/SP-",
    ]
    result = c.run(" ".join(cmd))
    assert (result is not None) and (result.return_code == 0)
    assert (INSTALL_PATH / INNO_APP_EXE.name).exists(), f"'{INSTALL_PATH / INNO_APP_EXE.name}' not found after installation"
    assert (INSTALL_PATH / INNO_APP_GUI_EXE.name).exists(), f"'{INSTALL_PATH / INNO_APP_GUI_EXE.name}' not found after installation"
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


@task(pre=[install_app,], post=[uninstall_app,])  # pyright: ignore[reportUntypedFunctionDecorator]
def check(c: InvokeContext):
    base.check(c, exe=INSTALL_PATH / f"{INNO_APP_EXE.name}")  # pyright: ignore[reportUnknownMemberType]
    base.check(c, exe=INSTALL_PATH / f"{INNO_APP_GUI_EXE.name}")  # pyright: ignore[reportUnknownMemberType]
