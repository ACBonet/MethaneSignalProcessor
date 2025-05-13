
bat_content = """\
@echo off
REM build_windows_safe.bat
REM This script compiles main.py into dist\\main.exe using PyInstaller.
REM The resulting .exe expects raw_data to be at the same level as the dist/ folder.

echo 🔍 Checking Python installation...
where python >nul 2>nul || (
    echo ❌ Python is not installed or not in PATH.
    pause
    exit /b
)

echo 🔍 Checking pip...
where pip >nul 2>nul || (
    echo ❌ pip is not installed or not in PATH.
    echo 💡 You may need to reinstall Python and select "Add to PATH" during setup.
    pause
    exit /b
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🛠 Compiling CH4 executable...
python -m PyInstaller --onefile --add-data "Raw data;Raw data" main.py

echo ✅ Done!
echo 📂 Your executable is now located at dist\\main.exe
echo 📁 It expects raw_data to be found at the same level as dist\\
pause
"""

bat_path = "/mnt/data/build_exe.bat"
with open(bat_path, "w") as f:
    f.write(bat_content)

bat_path