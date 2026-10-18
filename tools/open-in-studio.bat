@echo off
rem Blind Vow: build the place from this repository with Rojo and open it in Roblox Studio.
rem Works without the Rojo Studio plugin. Run it again after every code change.
cd /d "%~dp0.."
set "ROJO=rojo"
where rojo >nul 2>&1 || set "ROJO=%~dp0..\..\rojo.exe"
if not exist "%ROJO%" if not "%ROJO%"=="rojo" (
  echo Khong tim thay rojo.exe. Dat rojo.exe vao thu muc chua kho (canh thu muc Blind-vow-^).
  pause
  exit /b 1
)
"%ROJO%" build default.project.json -o BlindVow.rbxl > tools\open-in-studio.log 2>&1
if errorlevel 1 (
  type tools\open-in-studio.log
  echo LOI khi build. Gui noi dung tren cho Claude.
  pause
  exit /b 1
)
start "" "%CD%\BlindVow.rbxl"
