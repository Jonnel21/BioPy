; -- Example2.iss --
; Same as Example1.iss, but creates its icon in the Programs folder of the
; Start Menu instead of in a subfolder, and also creates a desktop icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=BioPy
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\BioPy
; Since no icons will be created in "{group}", we don't need the wizard
; to ask for a Start Menu folder name:
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\MyProg.exe
Compression=lzma2
SolidCompression=yes
OutputDir= .

[Files]
Source: "C:\Users\Jonnel\Desktop\BioPy\dist\gui\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\BioPy"; Filename: "{app}\gui.exe"
Name: "{autodesktop}\BioPy"; Filename: "{app}\gui.exe"
