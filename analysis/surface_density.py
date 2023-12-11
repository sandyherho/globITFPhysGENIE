#!/usr/bin/env python

"""
Surface Density Data Analysis and Visualization

Author: S. H. S. Herho
Email: sandy.herho@email.ucr.edu
Date: 12/08/23

This script loads oceanographic data from NetCDF files, performs basic statistical
analysis, generates visualizations, and conducts statistical tests on surface density values.

"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cmocean.cm as cm
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp

# Set the plot style
plt.style.use("ggplot")

def load_data(file_path):
    """
    Load oceanographic data from NetCDF file.

    Parameters:
        file_path (str): Path to the NetCDF file.

    Returns:
        tuple: Tuple containing lon, lat, and rho arrays.
    """
    ds = xr.open_dataset(file_path)
    lon = ds["lon"].to_numpy()
    lat = ds["lat"].to_numpy()
    rho = ds["phys_ocn_rho"].isel(time=0, zt=0)
    return lon, lat, rho

def calculate_stats_and_plot(lon, lat, rho, title, save_path):
    """
    Calculate statistics and generate contour plot.

    Parameters:
        lon (np.ndarray): Longitudes.
        lat (np.ndarray): Latitudes.
        rho (xr.DataArray): Density values.
        title (str): Title for statistics.
        save_path (str): File path to save the plot.
    """
    mean_value = rho.mean().values
    median_value = rho.median().values
    max_value = rho.max().values
    min_value = rho.min().values

    print(f"{title} Statistics:")
    print(f"Mean: {mean_value}\nMedian: {median_value}\nMax: {max_value}\nMin: {min_value}\n")

    plt.fill_between(lon, lat.min(), lat.max(), color='#988558')
    contour_filled = plt.contourf(lon, lat, rho, cmap=cm.algae)
    contour_lines = plt.contour(lon, lat, rho, colors='k', linewidths=0.2)

    plt.xlabel(r"Longitude [$^{\circ}$E]", fontsize=16)
    plt.ylabel(r"Latitude [$^{\circ}$N]", fontsize=16)

    cbar = plt.colorbar(contour_filled)
    cbar.set_label(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.1f')

    plt.tight_layout()
    plt.savefig(save_path, dpi=600)

def plot_box_and_kde(open_rho, close_rho, save_path):
    """
    Generate boxplot and KDE plots.

    Parameters:
        open_rho (np.ndarray): Density values for open dataset.
        close_rho (np.ndarray): Density values for closed dataset.
        save_path (str): File path to save the plot.
    """
    combined_data = np.concatenate([open_rho, close_rho])
    grouping_array = np.concatenate([['Open'] * len(open_rho), ['Closed'] * len(close_rho)])

    sns.boxplot(x=grouping_array, y=combined_data)
    plt.ylabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.tight_layout()
    plt.savefig(save_path, dpi=600)

    sns.kdeplot(open_rho, label='Open', fill=False)
    sns.kdeplot(close_rho, label='Closed', fill=False)
    plt.xlabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.ylabel('Probability Density', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig("../figs/fig1e.png", dpi=600)

def perform_statistical_tests(open_rho, close_rho):
    """
    Perform Mann-Whitney U and KS tests.

    Parameters:
        open_rho (np.ndarray): Density values for open dataset.
        close_rho (np.ndarray): Density values for closed dataset.
    """
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

def plot_ecdfs(open_rho, close_rho):
    """
    Plot ECDFs for open and closed datasets.

    Parameters:
        open_rho (np.ndarray): Density values for open dataset.
        close_rho (np.ndarray): Density values for closed dataset.
    """
    # Calculate ECDFs
    def ecdf(data):
        sorted_data = np.sort(data)
        n = len(data)
        y = np.arange(1, n + 1) / n
        return sorted_data, y

    x1, y1 = ecdf(open_rho)
    x2, y2 = ecdf(close_rho)

    # Plot ECDFs
    plt.plot(x1, y1, label='Open')
    plt.plot(x2, y2, label='Closed')
    plt.xlabel(r"$\rho$ (kg/m$^3$)", fontsize=16)
    plt.ylabel('ECDFs', fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig("../figs/fig1f.png", dpi=600)

def main():
    open_file_path = "../data/open/fields_biogem_3d.nc"
    closed_file_path = "../data/closed/fields_biogem_3d.nc"

    lon_open, lat_open, rho_open = load_data(open_file_path)
    lon_closed, lat_closed, rho_closed = load_data(closed_file_path)

    # Calculate anomalies
    rho_anom = rho_closed - rho_open

    # Plotting
    calculate_stats_and_plot(lon_open, lat_open, rho_open, "Open", "../figs/fig1a.png")
    calculate_stats_and_plot(lon_closed, lat_closed, rho_closed, "Closed", "../figs/fig1b.png")
    calculate_stats_and_plot(lon_closed, lat_closed, rho_anom, "Anomaly", "../figs/fig1c.png")

    # Other plots and analyses
    open_rho = rho_open.values.flatten()
    close_rho = rho_closed.values.flatten()

    open_rho = open_rho[~(np.isnan(open_rho))]
    close_rho = close_rho[~(np.isnan(close_rho))]

    plot_box_and_kde(open_rho, close_rho, "../figs/fig1d.png")
    perform_statistical_tests(open_rho, close_rho)
    plot_ecdfs(open_rho, close_rho)

if __name__ == "__main__":
    main()
