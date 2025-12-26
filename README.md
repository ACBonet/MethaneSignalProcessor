MethaneSignalProcessor (MSP)
====================

MethaneSignalProcessor (MSP) is an open-source tool for processing high-frequency CH₄ (methane) concentration time-series acquired with floating chambers.
The routine separates diffusive and ebullitive emission components, applies advanced signal correction, and exports numerical summaries together with graphical outputs.

📦 Project Overview
-------------------
MSP is designed to support automated, standardized, and reproducible analysis of aquatic methane signals, particularly those obtained with low-cost sensors under field conditions.

Main capabilities:
- Automated data cleaning and preprocessing
- Advanced digital filtering
- Adaptive peak detection for ebullition events
- Dual-branch correction with multi-scale refinement
- Regression-based diffusive flux estimation
- Structured export of numerical results and figures

📁 Project Contents
-------------------

    MethaneSignalProcessor (MSP)
    ├── main.py                  # Main CLI entry point
    ├── inc/functions.py         # Core processing logic
    ├── Raw data/                # Input .txt files
    ├── Processed data/          # Output data and figures
    │   ├── data/                # Processed .csv files
    │   ├── results/             # Text summaries (fluxes & bubbles)
    │   └── plots/               # Output figures
    ├── example_outputs/         # Example outputs for reference
    ├── build_exe.bat            # Script to build Windows executable
    ├── requirements.txt         # Python dependencies
    └── README.md                # Project documentation

---

## 🧰 Requirements

- Python ≥ 3.8  
- pip (Python package manager)

To build the Windows executable, **PyInstaller** is required (handled automatically by `build_exe.bat`).

---

## 🚀 Quick Start

### Option 1 — Python (Linux / macOS / Windows)
1. Clone the repository:
```bash
git clone https://github.com/ACBonet/MethaneSignalProcessor.git
cd MethaneSignalProcessor
```

2.	(Optional but recommended) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```.
3.	Install dependencies:
```bash
pip install -r requirements.txt
```

4.	Run the processor:
```bash
python main.py
```

### Option 2 — Windows Executable (.exe)
After compilation, simply double-click:
```bash
CH4Processor.exe
```
or run it from the terminal.

The program will prompt you to:
	•	Process a single .txt file, or
	•	Process all .txt files located in the Raw data/ folder

Outputs are automatically written to the Processed data/ directory.

## 🪟 Building the Windows Executable

To generate the executable from source:
	1.	Install Python from https://www.python.org
(ensure “Add Python to PATH” is checked)
	2.	Open the project folder
	3.	Double-click build_exe.bat
(or run it from the terminal)

The executable CH4Processor.exe will be created.
It expects the folders Raw data/ and Processed data/ to be located at the same level.

## 🧪 Usage Summary

### Run one of the following:
```bash
python main.py        # Python usage
CH4Processor.exe      # Executable usage
```
### The tool will:
- Load .txt files from Raw data/
- Apply filtering, peak detection, and correction
- Export results to Processed data/, including:

### Numerical Outputs
- Text summaries of diffusive flux segments
- Summary statistics of diffusive fluxes
- Ebullitive event metrics (counts, rates, relative contribution)

### Graphical Outputs
Saved in Processed data/plots/:
- Original vs processed signal with detected peaks
- Step-like representation of ebullitive events
- Linear fits on diffusive segments (with slope and R²)
    
## 📊 Example Outputs

Representative outputs can be previewed in the example_outputs/ folder.

These include:
- Detected peaks overlaid on raw and corrected signals
- Step-wise reconstruction of ebullitive dynamics
- Linear regression fits on diffusive segments

## 📄 Example Numerical Summary

Each processed file generates a text report (e.g. example_results.txt) containing:



These outputs support both quantitative analysis and visual inspection.

## ⚙️ Input File Format

Input .txt files must include:
- A time column (regularly sampled)
- A CH₄ concentration column (ppm)
- Optional temperature and pressure columns

Example input files are provided in the Raw data/ folder.

## 🧯 Troubleshooting

### ModuleNotFoundError
- Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```
### Executable does not find input files
- Confirm Raw data/ is in the same directory as CH4Processor.exe

### Unexpected or noisy results
- Verify input data formatting and sampling consistency
- Extremely low-amplitude or highly noisy signals may reduce peak detection reliability

## 📌 Methodological Scope and Limitations
- MSP is designed for time-series CH₄ data acquired with floating chambers.
- The pipeline assumes quasi-steady diffusive accumulation between ebullition events.
- Strong hydrodynamic forcing, rapid environmental transitions, or highly turbulent conditions may introduce non-linearities not captured by linear regression.
- MSP provides automated signal decomposition and relative flux estimates; absolute flux accuracy depends on sensor calibration, chamber geometry, and environmental conditions.
- Validation against independent reference methods (e.g. GC-based measurements) should be considered when available.

## 📜 License & Citation

This project is released as open-source.

If you use MSP in your work, please cite the associated publication
(to be updated upon acceptance).
