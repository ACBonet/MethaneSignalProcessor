bat_content = """\
@echo off
REM build_exe.bat
REM Compiles main.py into CH4Processor.exe in the project root directory

echo Checking Python installation...
where python >nul 2>nul || (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

echo Checking pip...
where pip >nul 2>nul || (
    echo pip is not installed or not in PATH.
    echo You may need to reinstall Python and select "Add to PATH" during setup.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt

echo Compiling executable as CH4Processor.exe in the current folder...
python -m PyInstaller --onefile --name CH4Processor --distpath . --add-data "Raw data;Raw data" main.py

echo Done!
echo You can now run CH4Processor.exe from this directory.
pause
"""

bat_path = "/mnt/data/build_exe.bat"
with open(bat_path, "w") as f:
    f.write(bat_content)

bat_path