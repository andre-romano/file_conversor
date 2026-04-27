
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=File Conversor
AppVersion={#AppVersion}
DefaultDirName={autopf}/file_conversor
Compression=lzma2/max
SolidCompression=yes
ShowLanguageDialog=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
LicenseFile=.\LICENSE
InfoBeforeFile=.\NOTICE
SetupIconFile=.\config\icons\icon.ico
UninstallDisplayIcon={app}\icon.ico
SourceDir=.
OutputDir={#OutputDir}
OutputBaseFilename={#OutputFilename}

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: cli; Description: Command-line interface (CLI); Types: full compact
Name: gui; Description: Graphical user interface (GUI); Types: full
Name: plugins; Description: Plugins; Types: full

[Tasks]
Name: desktop_icon; Description: Create desktop icon; Components: gui
Name: start_menu_icon; Description: Create start menu icon; Components: gui
Name: ctx_menu; Description: Install context menu entries; Components: cli; Flags: restart

[Dirs]
Name: "{app}"; Permissions: everyone-full

[Files]
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion allowunsafefiles
Source: "NOTICE"; DestDir: "{app}"; Flags: ignoreversion allowunsafefiles
Source: "THIRD_PARTY_LICENSES.md"; DestDir: "{app}"; Flags: ignoreversion allowunsafefiles
Source: "configs"; DestDir: "{app}"; Flags: ignoreversion allowunsafefiles recursesubdirs
Source: "build\windows-amd64\file_conversor.exe"; DestDir: "{app}"; Components: cli; Flags: ignoreversion allowunsafefiles
Source: "build\windows-amd64\file_conversor_gui.exe"; DestDir: "{app}"; Components: gui; Flags: ignoreversion allowunsafefiles

[Registry]
; Adds app_folder to the USER PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{olddata};{app}"; Flags: preservestringtype; Check: not IsAdmin()

; Adds app_folder to the SYSTEM PATH (requires admin privileges)
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "PATH"; ValueData: "{olddata};{app}"; Flags: preservestringtype; Check: IsAdmin()

[Icons]
Name: "{group}\File Conversor"; Filename: "{app}\file_conversor_gui.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: start_menu_icon
Name: "{autodesktop}\File Conversor"; Filename: "{app}\file_conversor_gui.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktop_icon

[Run]
StatusMsg: "Installing file_conversor context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{app}\file_conversor.exe"" win install-menu"""; WorkingDir: "{app}"; Tasks: ctx_menu; Flags: runhidden runascurrentuser waituntilterminated

[UninstallRun]
StatusMsg: "Uninstalling file_conversor context menu ..."; Filename: "cmd.exe"; Parameters: "/C """"{app}\file_conversor.exe"" win uninstall-menu"""; WorkingDir: "{app}"; Tasks: ctx_menu; Flags: runhidden runascurrentuser waituntilterminated; RunOnceId: "uninstall_menu"
StatusMsg: "Clean up files ..."; Filename: "cmd.exe"; Parameters: "/C rmdir /s /q ""{app}"""; Flags: runhidden runascurrentuser; RunOnceId: "cleanup_files"

