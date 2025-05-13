@echo off
echo Checking Python installation...
where python >nul 2>nul || (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Compiling CH4 executable...
pyinstaller --onefile --add-data "Raw data;Raw data" main.py

echo Done! Executable created at dist\main.exe
pause