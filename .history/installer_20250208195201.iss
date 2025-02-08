; Inno Setup script for RenameArrr Windows installer

[Setup]
AppName=RenameArrr
AppVersion=1.0.0
AppPublisher=RenameArrr Team
AppPublisherURL=https://github.com/feliciien/Rename-arrr-Post-arrr
AppSupportURL=https://github.com/feliciien/Rename-arrr-Post-arrr/issues
AppUpdatesURL=https://github.com/feliciien/Rename-arrr-Post-arrr/releases
DefaultDirName={autopf}\RenameArrr
DefaultGroupName=RenameArrr
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=RenameArrrInstaller
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\RenameArrr.exe
PrivilegesRequired=admin
WizardStyle=modern

[Files]
Source: "dist\RenameArrr.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "rename_arrr\license_manager.py"; DestDir: "{app}\rename_arrr"; Flags: ignoreversion
Source: "rename_arrr\core\*"; DestDir: "{app}\rename_arrr\core"; Flags: ignoreversion recursesubdirs
Source: "rename_arrr\gui\*"; DestDir: "{app}\rename_arrr\gui"; Flags: ignoreversion recursesubdirs
Source: "rename_arrr\scrapers\*"; DestDir: "{app}\rename_arrr\scrapers"; Flags: ignoreversion recursesubdirs

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Icons]
Name: "{group}\RenameArrr"; Filename: "{app}\RenameArrr.exe"
Name: "{group}\Uninstall RenameArrr"; Filename: "{uninstallexe}"
Name: "{commondesktop}\RenameArrr"; Filename: "{app}\RenameArrr.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: checked

[Run]
Filename: "{app}\RenameArrr.exe"; Description: "Launch RenameArrr"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\rename_arrr"
Type: files; Name: "{app}\rename_count.json"
