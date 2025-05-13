CH₄ Signal Processor
====================

This project provides a tool to process CH₄ (methane) concentration data from `.txt` files, apply advanced filtering and peak correction, and export cleaned `.txt` files along with visualizations.

📁 Project Contents
-------------------

📦 CH4 Signal Processor
├── main.py                 # Main CLI entry point
├── inc/functions.py       # Processing logic
├── Raw data/              # Input .txt files
├── Processed data/        # Output .txt and plots
├── dist/                  # Compiled executable output
├── build_exe.bat      # Script to build .exe using PyInstaller
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

🧰 Requirements
---------------

- Python ≥ 3.8
- pip (Python package manager)
- Git (to clone the repository)

> To build the `.exe`, PyInstaller must be installed (automatically handled by the `.bat` script).

🪟 How to Use on Windows
------------------------

🔹 Option 1 – Use the `.exe`

After compilation, simply double-click `main.exe` located in the `dist/` folder, or run it from the terminal:

    dist\main.exe

You’ll be prompted to choose whether to process a specific file or all `.txt` files in the `Raw data/` folder.  
The processed data will be saved in `Processed data/`.

🔹 Option 2 – Compile the `.exe` with `build_windows.bat`

To generate the executable from source:

1. Install Python from https://www.python.org and make sure to check "Add to PATH"
2. Open the project folder
3. Double-click `build_windows.bat`
   (or run it from terminal: `.uild_windows.bat`)

This will create the executable at `dist/main.exe`.  
It expects the `Raw data/` folder to be at the same level as `dist/`.

🧪 Usage Instructions
---------------------

Run from the terminal (depending on version used):

    python main.py --dir .         # for direct Python usage
    dist\main.exe                 # for the compiled executable

The tool will:

- Load `.txt` files from `Raw data/`
- Apply signal filtering and peak correction
- Save processed results and plots to `Processed data/`

🧼 Notes
--------

- The executable assumes the folder structure is preserved (`dist/` next to `Raw data/`)
- A `.gitignore` file is included to avoid committing generated files


