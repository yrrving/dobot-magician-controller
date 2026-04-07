Windows build kit for Dobot Magician.

Contents:
- requirements-windows.txt
- build_windows.bat
- ..\source\dobot_ui.py

How to build on a Windows PC:
1. Install Python 3.
2. Open Command Prompt in this folder.
3. Run: build_windows.bat
4. The finished app is created in:
   windows\dist\DobotKontroll_PC.exe

Notes:
- The code is prepared for Windows COM ports and macOS USB serial ports.
- Build the EXE on Windows, not on Mac.
- If Windows Defender warns on first run, choose More info -> Run anyway if needed.
