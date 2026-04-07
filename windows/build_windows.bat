@echo off
setlocal

cd /d %~dp0

if not exist ..\source\dobot_ui.py (
  echo Could not find ..\source\dobot_ui.py
  exit /b 1
)

py -m pip install --upgrade pip
py -m pip install -r requirements-windows.txt

py -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onefile ^
  --name DobotKontroll_PC ^
  ..\source\dobot_ui.py

echo.
echo Build complete.
echo EXE should be here:
echo %cd%\dist\DobotKontroll_PC.exe
