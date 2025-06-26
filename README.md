Calcium Decay Analysis
======================

This repository provides code for analyzing calcium imaging data, including:
- Fitting one-phase exponential decay curves to each cell trace
- Baseline correction
- Z-score normalization
- Plotting mean ± SEM for raw, fitted, and normalized signals

Files Included:
---------------
- calcium_decay_analysis.py              # Python script for command-line use
- calcium_decay_analysis_notebook.ipynb  # Jupyter or Hex notebook for interactive analysis
- requirements.txt                       # List of required Python libraries

Requirements:
-------------
You need Python 3.x with the following packages:
- numpy
- pandas
- matplotlib
- scipy

Install dependencies with:
    pip install -r requirements.txt

How to Use:
-----------

1. Prepare your data file (CSV format, no header). Place it in the project directory.

2. Run the Python script from the command line:
    python calcium_decay_analysis.py --file yourdata.csv --sampling_rate 5.0 --puff_idx 505

    - Replace "yourdata.csv" with your actual data file name.
    - "--sampling_rate" (optional) sets your sample rate in Hz (default: 5.0)
    - "--puff_idx" (optional) sets the index for the puff/stimulus (default: 505)

3. OR, run the notebook:
    - Open "calcium_decay_analysis_notebook.ipynb" in Jupyter Lab, Jupyter Notebook, or Hex.
    - Upload your data file to the notebook environment if needed.
    - Run the notebook cells step by step.

Repository Structure (example):
------------------------------
README.txt
requirements.txt
calcium_decay_analysis.py
calcium_decay_analysis_notebook.ipynb

Notes:
------
- Example data is not provided. Use your own CSV-formatted calcium trace data.
- The notebook version is ideal for interactive exploration, parameter tweaking, and visualization.

Contact:
--------
Questions? Open an issue or pull request on GitHub.

Author:
-------
Mollie Bernstein, 2025
