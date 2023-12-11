#!/usr/bin/env python

"""
Ventilation Age Data Analysis and Visualization

Author: S. H. S. Herho
Email: sandy.herho@email.ucr.edu
Date: 12/08/23

This script loads oceanographic data from NetCDF files, performs basic statistical
analysis, generates visualizations, and conducts statistical tests on ventilation age data
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cmocean.cm as cm
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp
plt.style.use("ggplot")

def plot_contour(lat, zt, psi, filename):
    """
    Plot contour plot for given latitude, depth, and streamfunction data.
    """
    plt.fill_between(lat, zt.min(), zt.max(), color='#695447')
    contour_filled = plt.contourf(lat, zt, psi, cmap=cm.balance)
    contour_lines = plt.contour(lat, zt, psi, colors='k', linewidths=0.5)

    plt.xlabel("Latitude [°N]", fontsize=16)
    plt.ylabel("Depth [m]", fontsize=16)
    cbar = plt.colorbar(contour_filled)
    cbar.set_label(r"$\psi$ (Sv)", fontsize=16)
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.1f')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(filename, dpi=600)

def plot_distribution_comparison(data1, label1, data2, label2, filename):
    """
    Plot KDE comparison for two datasets.
    """
    sns.kdeplot(data1, label=label1, fill=False)
    sns.kdeplot(data2, label=label2, fill=False)
    plt.xlabel(r"$\psi$ (Sv)", fontsize=16)
    plt.ylabel('Probability Density', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=600)

def perform_and_interpret_tests(data1, label1, data2, label2):
    """
    Perform statistical tests (Mann-Whitney U and KS) and interpret the results.
    """
    statistic_mw, p_value_mw = mannwhitneyu(data1, data2)
    statistic_ks, p_value_ks = ks_2samp(data1, data2)

    print(f'Mann-Whitney U test: {label1} vs {label2}')
    print(f'Statistic: {round(statistic_mw, 3)}, p-value: {round(p_value_mw, 3)}')
    print(f'KS test: {label1} vs {label2}')
    print(f'Statistic: {round(statistic_ks, 3)}, p-value: {round(p_value_ks, 3)}')

    if p_value_mw < 0.05 or p_value_ks < 0.05:
        print('The distributions are significantly different.')
    else:
        print('No significant difference between the distributions.')

def plot_ecdfs(data1, label1, data2, label2, filename):
    """
    Plot ECDFs for two datasets.
    """
    x1, y1 = ecdf(data1)
    x2, y2 = ecdf(data2)

    plt.plot(x1, y1, label=label1)
    plt.plot(x2, y2, label=label2)
    plt.xlabel(r"$\psi$ (Sv)", fontsize=16)
    plt.ylabel('ECDFs', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=600)

def ecdf(data):
    """
    Calculate empirical cumulative distribution function (ECDF) for given data.
    """
    sorted_data = np.sort(data)
    n = len(data)
    y = np.arange(1, n + 1) / n
    return sorted_data, y

if __name__ == "__main__":
    # Data loading and processing
    ds_open = xr.open_dataset("../data/open/fields_biogem_2d.nc")
    ds_close = xr.open_dataset("../data/closed/fields_biogem_2d.nc")

    zt_open = ds_open["zt_moc"].to_numpy()
    lat_open = ds_open["lat_moc"].to_numpy()
    psi_open = ds_open["phys_opsi"].isel(time=0)

    zt_close = ds_close["zt_moc"].to_numpy()
    lat_close = ds_close["lat_moc"].to_numpy()
    psi_close = ds_close["phys_opsi"].isel(time=0)

    psi_anom = psi_close - psi_open

    # Plotting contour plots
    plot_contour(lat_open, zt_open, psi_open, "../figs/fig3a.png")
    plot_contour(lat_close, zt_close, psi_close, "../figs/fig3b.png")
    plot_contour(lat_close, zt_close, psi_anom, "../figs/fig3c.png")

    # Flatten and clean data
    open_psi = psi_open.to_numpy().flatten()
    close_psi = psi_close.to_numpy().flatten()

    open_psi = open_psi[~(np.isnan(open_psi))]
    close_psi = close_psi[~(np.isnan(close_psi))]

    # Plotting KDE comparison
    plot_distribution_comparison(open_psi, 'Open', close_psi, 'Closed', "../figs/fig3e.png")

    # Plotting boxplot
    combined_data = np.concatenate([open_psi, close_psi])
    grouping_array = np.concatenate([['Open'] * len(open_psi), ['Closed'] * len(close_psi)])
    sns.boxplot(x=grouping_array, y=combined_data)
    plt.ylabel(r"$\psi$ (Sv)", fontsize=16)
    plt.tight_layout()
    plt.savefig("../figs/fig3d.png", dpi=600)

    # Statistical tests and interpretation
    perform_and_interpret_tests(open_psi, 'Open', close_psi, 'Closed')

    # Plotting ECDFs
    plot_ecdfs(open_psi, 'Open', close_psi, 'Closed', "../figs/fig3f.png")
