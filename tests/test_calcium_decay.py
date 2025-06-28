import numpy as np
import pandas as pd
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from calcium_decay_analysis import fit_one_phase_decay, calculate_zscores
from preprocess import subset_fluorescence


def test_fit_one_phase_decay_shapes():
    time = np.linspace(0, 10, 50)
    # create decaying signals for 3 cells
    data = np.exp(-0.3 * time)[:, None] * np.ones((1, 3))
    noise = 0.01 * np.random.randn(*data.shape)
    raw = data + noise
    params, fitted = fit_one_phase_decay(time, raw)
    assert params.shape == (3, 3)
    assert fitted.shape == raw.shape


def test_calculate_zscores_shape():
    corrected = np.random.rand(100, 4)
    z = calculate_zscores(corrected, puff_idx=50, fs=5.0)
    assert z.shape == corrected.shape
    assert not np.isnan(z).any()


def test_subset_fluorescence_shape():
    # create fake dataframe with puff index and 2000 samples
    n_cells = 3
    puff_index = 1000
    values = {}
    for i in range(n_cells):
        series = pd.Series([puff_index] + list(np.arange(1, 2001)))
        values[i] = series
    df = pd.DataFrame(values)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = f"{tmpdir}/raw.csv"
        output_path = f"{tmpdir}/subset.csv"
        df.to_csv(input_path, index=False, header=False)
        subset_fluorescence(input_path, output_path)
        subset = pd.read_csv(output_path, header=None)
    assert subset.shape == (1101, n_cells)
    assert (subset.iloc[0] == 501).all()
