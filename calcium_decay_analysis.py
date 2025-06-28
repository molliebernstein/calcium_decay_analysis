"""
calcium_decay_analysis.py

Analyze and plot calcium fluorescence traces:
- Loads raw data from a CSV file (cells x time).
- Plots raw trace (mean ± SEM).
- Fits one-phase exponential decay to each cell.
- Subtracts decay from raw traces.
- Calculates z-scores (baseline: 10s before stimulus).
- Plots summary figures.

Author: Mollie Bernstein
Date: 2025-06-26

Requirements:
    numpy
    pandas
    matplotlib
    scipy

Usage:
    python calcium_decay_analysis.py --file sgRosa26_30uM_DHPG_puff_processed.csv --sampling_rate 5.0 --puff_idx 505
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import argparse

def one_phase_decay(t, A, k, C):
    """One-phase exponential decay function."""
    return A * np.exp(-k * t) + C

def load_data(file_name):
    """Load CSV file and clean up infinities/NaNs."""
    data = pd.read_csv(file_name, header=None)
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    return data.values

def plot_mean_sem(time, mean, sem, color, ylabel, title, label):
    """Plot mean ± SEM as fill."""
    plt.figure(figsize=(10, 6))
    plt.fill_between(time, mean - sem, mean + sem, color=color, alpha=0.3,
                     label='SEM')
    plt.plot(time, mean, color + '-', label=label)
    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()

def fit_one_phase_decay(time, raw):
    """Fit one-phase exponential decay to each cell trace."""
    n_points, n_cells = raw.shape
    params = np.zeros((n_cells, 3))
    fitted_curves = np.zeros((n_points, n_cells))
    for i in range(n_cells):
        y_data = raw[:, i]
        A_guess = y_data[0] - y_data[-1]
        k_guess = 0.01
        C_guess = y_data[-1]
        p0 = [A_guess, k_guess, C_guess]
        try:
            popt, _ = curve_fit(one_phase_decay, time, y_data, p0=p0, maxfev=10000)
        except RuntimeError:
            print(f"Fit did not converge for cell {i}")
            popt = [np.nan, np.nan, np.nan]
        params[i, :] = popt
        fitted_curves[:, i] = one_phase_decay(time, *popt)
    return params, fitted_curves

def calculate_zscores(corrected_signal, puff_idx, fs):
    """Calculate z-scores using 10s pre-puff as baseline."""
    baseline_start = max(0, puff_idx - int(10 * fs))
    baseline_end = min(corrected_signal.shape[0], puff_idx)
    n_points, n_cells = corrected_signal.shape
    zscores = np.zeros_like(corrected_signal)
    for i in range(n_cells):
        baseline = corrected_signal[baseline_start:baseline_end, i]
        base_mean = baseline.mean()
        base_std = baseline.std(ddof=1)
        if base_std == 0 or np.isnan(base_std):
            zscores[:, i] = np.nan
        else:
            zscores[:, i] = (corrected_signal[:, i] - base_mean) / base_std
    return zscores

def main(args):
    # --- Load Data ---
    raw = load_data(args.file)
    n_points, n_cells = raw.shape
    time = np.arange(n_points) / args.sampling_rate

    # --- Plot Raw Signal ---
    mean_raw = raw.mean(axis=1)
    sem_raw = raw.std(axis=1, ddof=1) / np.sqrt(n_cells)
    plot_mean_sem(time, mean_raw, sem_raw, 'k', 'Calcium Fluorescence', 'Raw Calcium Fluorescence Signal (Mean ± SEM)', 'Mean Raw Signal')

    # --- Fit One-Phase Decay ---
    params, fitted_curves = fit_one_phase_decay(time, raw)

    # --- Subtract Fitted Decay ---
    corrected_signal = raw - fitted_curves

    # Plot mean fitted decay
    mean_fit = fitted_curves.mean(axis=1)
    sem_fit = fitted_curves.std(axis=1, ddof=1) / np.sqrt(n_cells)
    plot_mean_sem(time, mean_fit, sem_fit, 'r', 'Fitted Decay', 'Fitted One‐Phase Decay (Mean ± SEM)', 'Mean Fitted Decay')

    # --- Z-scores (10s baseline before puff) ---
    zscores = calculate_zscores(corrected_signal, args.puff_idx, args.sampling_rate)

    mean_z = zscores.mean(axis=1)
    sem_z = zscores.std(axis=1, ddof=1) / np.sqrt(n_cells)
    plot_mean_sem(time, mean_z, sem_z, 'g', 'Z-score', 'Z-Scored Signal (Mean ± SEM)', 'Mean Z-score')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze calcium imaging trace with decay correction and z-score normalization.")
    parser.add_argument('--file', type=str, required=True, help="Path to CSV file (no header).")
    parser.add_argument('--sampling_rate', type=float, default=5.0, help="Sampling rate in Hz. Default: 5.0")
    parser.add_argument('--puff_idx', type=int, default=505, help="Index of puff/stimulus. Default: 505")
    args = parser.parse_args()
    main(args)
