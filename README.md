CH₄ Signal Processor
====================

This project provides a tool to process CH₄ (methane) concentration data from `.txt` files, apply advanced filtering, peak correction, and output clean `.txt` files and visualizations.

📁 Project Contents
-------------------

📦 CH4 Signal Processor
├── main.py                 # Main CLI entry point
├── inc/functions.py       # Processing logic
├── raw_data/              # Input .txt files
├── Processed data/        # Output .csv and plots
├── Dockerfile             # Build system for .exe
├── build_exe.sh / .bat    # Helpers for Docker build
├── requirements.txt       # Python dependencies
└── README.md              # This documentation

🧰 Requirements
---------------

- Python ≥ 3.8 (only for `.pyz` or local use)
- Docker Desktop (for compiling `.exe`)
- Git (to clone the repo)

🪟 How to use on Windows
-------------------------

🔹 Option 1 – Use the `.exe`

After compiling, just double-click the `.exe` or run in terminal:

    main.exe

You’ll be prompted whether to process a specific file or all files in `Raw data/`.

🔹 Option 2 – Compile the .exe with Docker (using build_exe.bat)

If you want to generate the .exe yourself from Windows using Docker:
	1.	Install Docker Desktop for Windows
	2.	Make sure Docker is running
	3.	Double-click the file build_exe.bat
(or run it from the terminal in the project folder)

🍏🐧 How to compile from macOS/Linux with Docker
------------------------------------------------

1. Make sure Docker is installed and running
   - https://www.docker.com/products/docker-desktop

2. Compile using the helper script:

    chmod +x build_exe.sh
    ./build_exe.sh

This will build the image and create the `.exe` inside `dist/main.exe`.

🧪 Usage instructions
---------------------

    python main.py --dir .             # for .py version
    ./main.exe                         # for .exe version

It will:
- Load `.txt` files from `raw_data/`
- Filter and correct CH₄ signals
- Save cleaned `.csv` and plots into `Processed data/`

🧼 Notes
--------

- The `.exe` is compiled using `cdrx/pyinstaller-windows` in Docker
- All output is saved to `Processed data/`
- A `.gitignore` is included to avoid committing generated files

