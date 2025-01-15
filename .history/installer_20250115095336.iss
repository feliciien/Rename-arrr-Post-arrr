; Inno Setup script for RenameArrr Windows installer

[Setup]
AppName=RenameArrr
AppVersion=1.0.0
DefaultDirName={pf}\RenameArrr
DefaultGroupName=RenameArrr
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=RenameArrrInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\RenameArrr.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\RenameArrr"; Filename: "{app}\RenameArrr.exe"
Name: "{autodesktop}\RenameArrr"; Filename: "{app}\RenameArrr.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: checked

[Run]
Filename: "{app}\RenameArrr.exe"; Description: "Launch RenameArrr"; Flags: nowait postinstall skipifsilent
