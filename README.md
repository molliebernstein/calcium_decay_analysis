Calcium Imaging Preprocessing and Analysis
==========================================

This repository contains tools for preprocessing and analyzing calcium imaging data from multiple subjects/cells.  
You will find scripts and notebook examples for:

- **Extracting fluorescence trace windows around a puff event** (preprocessing)
- **Calcium decay analysis and normalization** (decay fitting, baseline correction, z-scoring)
- Running from the command line or interactively in a notebook environment

----------------------------------------------------------------
Example Data
------------

Two example CSV files are provided:

1. sgRosa26_sgTrpc6_1uM_NTS_puffing_master_sheet.xlsx - raw_sgRosa26
    - For use with the window subsetting/preprocessing script.

2. sgRosa26_30uM_DHPG_puff_processed
    - For use with the calcium decay analysis script.

----------------------------------------------------------------
Scripts Included
----------------

1. **subset_preprocess.py**
    - Extracts a window of 500 values before and 600 after the puff event for each subject (column).
    - Input format: CSV where first row in each column is the puff index, rows 2+ are fluorescence values.
    - Puff event is centered at index 501 in the output.
    - Example usage:

        python preprocess.py --input "sgRosa26_sgTrpc6_1uM_NTS_puffing_master_sheet.xlsx - raw_sgRosa26.csv" --output subset_data.csv

    - Also provided as notebook-style cells for interactive use.

2. **calcium_decay_analysis.py**
    - For calcium decay correction, baseline correction, and z-score normalization.
    - Fits and subtracts one-phase decay for each cell, calculates z-scores using baseline, and plots results.
    - Input format: CSV of fluorescence (no header; each column is a cell).
    - Example usage:

        python calcium_decay_analysis.py --file "sgRosa26_30uM_DHPG_puff_processed.csv" --sampling_rate 5.0 --puff_idx 505

    - Also provided as a notebook for interactive analysis.

----------------------------------------------------------------
How to Use in a Notebook
------------------------

- Copy and paste the notebook cells from the README or `.ipynb` files.
- Upload the corresponding example CSV to your notebook environment.
- Run cells step by step; outputs and saved files will be shown or downloaded as needed.

----------------------------------------------------------------
Requirements
------------

Python 3.x with:

- numpy
- pandas
- matplotlib
- scipy

Install with:
    pip install -r requirements.txt

----------------------------------------------------------------
Repository Structure (example)
-----------------------------

README.txt
requirements.txt
preprocess.py
calcium_decay_analysis.py
preprocess.ipynb
calcium_decay_analysis.ipynb
sgRosa26_sgTrpc6_1uM_NTS_puffing_master_sheet.xlsx - raw_sgRosa26.csv
sgRosa26_30uM_DHPG_puff_processed.csv

----------------------------------------------------------------
Contact & Author
----------------

Questions? Open an issue or pull request on GitHub.

Author: Mollie Bernstein, 2025
