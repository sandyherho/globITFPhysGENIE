#!/usr/bin/env python

"""
Vertical Density Data Analysis and Visualization

Author: S. H. S. Herho
Email: sandy.herho@email.ucr.edu
Date: 12/08/23

This script loads oceanographic data from NetCDF files, performs basic statistical
analysis, generates visualizations, and conducts statistical tests on vertical density values.
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cmocean.cm as cm
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp
plt.style.use("ggplot")

def print_stats_and_plot(rho, label, filename):
    """
    Print statistics and plot contour for the given density field.

    Parameters:
    - rho (xarray.DataArray): Density field
    - label (str): Label for the dataset (e.g., "Open", "Closed", "Anomaly")
    - filename (str): File name for saving the contour plot
    """
    # Print statistics
    print(f"{label} Statistics:")
    print(f"Mean: {rho.mean().values}")
    print(f"Median: {rho.median().values}")
    print(f"Max: {rho.max().values}")
    print(f"Min: {rho.min().values}")

    # Plot contour
    plt.fill_between(rho.lat, rho.zt.min(), rho.zt.max(), color='#695447')
    contour_filled = plt.contourf(rho.lat, rho.zt, rho, cmap=cm.haline)
    contour_lines = plt.contour(rho.lat, rho.zt, rho, colors='k', linewidths=0.5)

    plt.xlabel("Latitude [°N]", fontsize=16)
    plt.ylabel("Depth [m]", fontsize=16)
    cbar = plt.colorbar(contour_filled)
    cbar.set_label(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.1f')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(filename, dpi=600)
    plt.show()

def plot_boxplot_and_kde(open_rho, close_rho):
    """
    Plot boxplot and KDE for the given density fields.

    Parameters:
    - open_rho (numpy.ndarray): Flattened density values for the "Open" dataset
    - close_rho (numpy.ndarray): Flattened density values for the "Closed" dataset
    """
    # Plot boxplot
    combined_data = np.concatenate([open_rho, close_rho])
    grouping_array = np.concatenate([['Open'] * len(open_rho), ['Closed'] * len(close_rho)])
    sns.boxplot(x=grouping_array, y=combined_data)
    plt.ylabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.tight_layout()
    plt.savefig("../figs/fig2d.png", dpi=600)
    plt.show()

    # Plot KDE
    sns.kdeplot(open_rho, label='Open', fill=False)
    sns.kdeplot(close_rho, label='Closed', fill=False)
    plt.xlabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.ylabel('Probability Density', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig("../figs/fig2e.png", dpi=600)
    plt.show()

def plot_ecdfs(open_rho, close_rho):
    """
    Plot ECDFs for the given density fields.

    Parameters:
    - open_rho (numpy.ndarray): Flattened density values for the "Open" dataset
    - close_rho (numpy.ndarray): Flattened density values for the "Closed" dataset
    """
    # Plot ECDFs
    x1, y1 = ecdf(open_rho)
    x2, y2 = ecdf(close_rho)

    plt.plot(x1, y1, label='Open')
    plt.plot(x2, y2, label='Closed')
    plt.xlabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.ylabel('ECDFs', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig("../figs/fig2f.png", dpi=600)
    plt.show()

def ecdf(data):
    """
    Calculate Empirical Cumulative Distribution Function (ECDF).

    Parameters:
    - data (numpy.ndarray): Input data

    Returns:
    - sorted_data (numpy.ndarray): Sorted input data
    - y (numpy.ndarray): ECDF values corresponding to sorted_data
    """
    sorted_data = np.sort(data)
    n = len(data)
    y = np.arange(1, n + 1) / n
    return sorted_data, y

if __name__ == "__main__":
    # Load datasets
    ds_open = xr.open_dataset("../data/open/fields_biogem_3d.nc")
    ds_close = xr.open_dataset("../data/closed/fields_biogem_3d.nc")

    # Extract variables
    zt_open = ds_open["zt"].to_numpy()
    lat_open = ds_open["lat"].to_numpy()
    rho_open = ds_open["phys_ocn_rho"].isel(time=0).mean(dim="lon")

    zt_close = ds_close["zt"].to_numpy()
    lat_close = ds_close["lat"].to_numpy()
    rho_close = ds_close["phys_ocn_rho"].isel(time=0).mean(dim="lon")

    # Calculate anomaly
    rho_anom = rho_close - rho_open

    # Print and plot statistics
    print_stats_and_plot(rho_open, "Open", "../figs/fig2a.png")
    print_stats_and_plot(rho_close, "Closed", "../figs/fig2c.png")
    print_stats_and_plot(rho_anom, "Anomaly", "../figs/fig2b.png")

    # Flatten density fields
    open_rho = rho_open.to_numpy().flatten()
    close_rho = rho_close.to_numpy().flatten()

    # Remove NaN values
    open_rho = open_rho[~np.isnan(open_rho)]
    close_rho = close_rho[~np.isnan(close_rho)]

    # Plot boxplot and KDE
    plot_boxplot_and_kde(open_rho, close_rho)

    # Mann-Whitney U test
    statistic_mw, p_value_mw = mannwhitneyu(open_rho, close_rho)
    print(f'Mann-Whitney U test statistic: {round(statistic_mw, 3)}')
    print(f'Mann-Whitney U test p-value: {round(p_value_mw, 3)}')

    # Interpretation of Mann-Whitney U test
    if p_value_mw < 0.05:
        print('The Mann-Whitney U test suggests a significant difference between the distributions of the two arrays.')
    else:
        print('The Mann-Whitney U test does not provide enough evidence to reject the null hypothesis of no difference between the distributions.')

    # Kolmogorov-Smirnov (KS) test
    statistic_ks, p_value_ks = ks_2samp(open_rho, close_rho)
    print(f'KS test statistic: {round(statistic_ks, 3)}')
    print(f'KS test p-value: {round(p_value_ks, 3)}')

    # Interpretation of KS test
    if p_value_ks < 0.05:
        print('The KS test suggests a significant difference between the distributions of the two arrays.')
    else:
        print('The KS test does not provide enough evidence to reject the null hypothesis of no difference between the distributions.')

    # Plot ECDFs
    plot_ecdfs(open_rho, close_rho)
