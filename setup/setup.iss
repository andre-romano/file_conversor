; -- setup.iss --
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=File Conversor
AppVersion=1.0.0
WizardStyle=modern
DefaultDirName={autopf}\File_Conversor
DefaultGroupName=File Conversor
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin 
ShowLanguageDialog=yes
SourceDir=.
OutputDir=..\dist
OutputBaseFilename=file_conversor_setup

[Files]
Source: "..\setup\*.ps1"; DestDir: "{tmp}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: "..\dist\file_conversor.exe"; DestDir: "{app}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: "..\data\*"; DestDir: "{app}\data"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles
Source: "..\locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles

; [Icons]
; Name: "{group}"; Filename: "{app}\file_conversor.exe"; Parameters: "gui"; WorkingDir: "{app}"; IconFilename: "{app}\data\icon.ico"
; Name: "{autodesktop}"; Filename: "{app}\file_conversor.exe"; Parameters: "gui"; WorkingDir: "{app}"; IconFilename: "{app}\data\icon.ico"

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File {tmp}\install_choco.ps1 -Verb RunAs"; StatusMsg: "Running PowerShell script..."; Check: NotIsChocoInstall

[UninstallDelete]
Type: files; Name: "{app}\*.*"


[Code]
var
  IsChoco: Boolean;

function IsChocoInstall(): Boolean;
begin
  Result := IsChoco;
end;

function NotIsChocoInstall(): Boolean;
begin
  Result := not IsChoco;
end;

function CmdLineParamsContain(param: String): Boolean;
begin
  Result := Pos(LowerCase(param), LowerCase(ExpandConstant('{cmdline}'))) > 0;
end;

function InitializeSetup(): Boolean;
begin
  // Check if custom /choco flag was passed
  IsChoco := CmdLineParamsContain('/choco');
  Result := True; // continue setup
end;