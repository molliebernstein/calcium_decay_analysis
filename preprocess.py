"""
preprocess.py

Extracts a window of fluorescence values around a puff event for each subject.

Usage:
    python subset_preprocess.py --input input.csv --output subset_data.csv

Assumes:
- Each column is a subject.
- First row of each column = puff index (integer).
- Rows 2+ = fluorescence data.

Output:
- CSV file of subsetted traces (puff event at index 501 in each column).
"""

import pandas as pd
import argparse


def subset_fluorescence(input_file, output_file):
    """Subset fluorescence traces around the puff event.

    Parameters
    ----------
    input_file : str
        Path to the CSV file containing raw fluorescence traces. The
        first row in each column is the puff index and subsequent rows
        contain the fluorescence values.
    output_file : str
        Destination path for the subsetted CSV file.
    """

    df = pd.read_csv(input_file, header=None)
    subset_columns = {}
    for col in df.columns:
        puff_index = int(df[col].iloc[0])
        fluorescence = df[col].iloc[1:].reset_index(drop=True)
        puff_event_idx = puff_index - 1
        start_idx = puff_event_idx - 500
        end_idx = puff_event_idx + 600
        subset_fluorescence = fluorescence.iloc[start_idx:end_idx].reset_index(
            drop=True
        )
        new_puff_index = 501
        new_column = pd.concat(
            [pd.Series([new_puff_index]), subset_fluorescence],
            ignore_index=True,
        )
        subset_columns[col] = new_column
    subset_df = pd.DataFrame(subset_columns)
    subset_df.to_csv(output_file, index=False, header=False)
    print(f"Subset dataframe created with shape: {subset_df.shape}")


def cli():
    """Command-line interface for the preprocessing module."""
    parser = argparse.ArgumentParser(
        description="Subset fluorescence around puff index for each column."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input CSV file path."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="subset_data.csv",
        help="Output CSV file name.",
    )
    args = parser.parse_args()
    subset_fluorescence(args.input, args.output)


if __name__ == "__main__":
    cli()
