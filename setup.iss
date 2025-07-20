; -- setup.iss --
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=File_Conversor
AppVersion=1.0.0
WizardStyle=modern
DefaultDirName={localappdata}\File_Conversor
DefaultGroupName=File_Conversor
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin 
ShowLanguageDialog=yes
SourceDir=.
OutputDir=.\dist
OutputBaseFilename=file_conversor_setup

[Files]
Source: ".\setup_run.ps1"; DestDir: "{tmp}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: ".\dist\*.exe"; DestDir: "{app}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: ".\data\*"; DestDir: "{app}\data"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: ".\locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles

[Icons]
Name: "{group}"; Filename: "{app}\file_conversor.exe"; Parameters: "gui"; WorkingDir: "{app}"; IconFilename: "{app}\data\icon.ico"
Name: "{autodesktop}"; Filename: "{app}\file_conversor.exe"; Parameters: "gui"; WorkingDir: "{app}"; IconFilename: "{app}\data\icon.ico"

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File {tmp}\setup_run.ps1 -Verb RunAs"; StatusMsg: "Running PowerShell script..."

[UninstallDelete]
Type: files; Name: "{app}\*.*"