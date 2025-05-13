CH₄ Signal Processor
====================

This project provides a tool to process CH₄ (methane) concentration data from `.txt` files, apply advanced filtering and peak correction, and export cleaned `.txt` files along with visualizations.

📁 Project Contents
-------------------

📦 CH4 Signal Processor
├── main.py                 # Main CLI entry point
├── inc/functions.py       # Processing logic
├── raw_data/              # Input .txt files
├── Processed data/        # Output .txt and plots
├── Dockerfile             # Docker build for Windows .exe
├── build_exe.sh / .bat    # Helper scripts for Docker build
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

🧰 Requirements
---------------

- Python ≥ 3.8 (only needed for `.py` or `.pyz` usage)
- Docker Desktop (for compiling the `.exe`)
- Git (for cloning the repository)

🪟 How to Use on Windows
-------------------------

🔹 Option 1 – Use the `.exe`

Once compiled, just double-click the `main.exe`, or run it from the terminal:

    main.exe

You’ll be prompted to choose whether to process a specific file or all `.txt` files inside the `Raw data/` folder.

🔹 Option 2 – Compile the `.exe` with Docker (`build_exe.bat`)

To build the executable from source on Windows:

1. Install Docker Desktop for Windows
2. Make sure Docker is running
3. Double-click `build_exe.bat`
   (or run it from the terminal inside the project folder)

The generated `.exe` will be saved to the `dist/` folder.

🍏🐧 How to Compile from macOS/Linux Using Docker
------------------------------------------------

1. Install Docker Desktop and ensure it's running
2. Open a terminal and run:

    chmod +x build_exe.sh
    ./build_exe.sh

This will build the Docker image and generate the `.exe` in `dist/main.exe`.

🧪 Usage Instructions
---------------------

Run from the terminal:

    python main.py --dir .             # for Python version
    ./main.exe                         # for Windows .exe version

The script will:

- Load `.txt` files from the `raw_data/` folder
- Apply signal filtering and peak correction
- Save cleaned `.txt` data and plots into `Processed data/`

🧼 Notes
--------

- The `.exe` is compiled using the `cdrx/pyinstaller-windows` Docker image
- All results are saved in `Processed data/`
- A `.gitignore` file is included to avoid tracking generated or system files


