#!/usr/bin/env python

"""
Global Overturning Circulation Data Analysis and Visualization

Author: S. H. S. Herho
Email: sandy.herho@email.ucr.edu
Date: 12/08/23

This script loads oceanographic data from NetCDF files, performs basic statistical
analysis, generates visualizations, and conducts statistical tests on global overturning circulations.
"""


import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cmocean.cm as cm
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp
plt.style.use("ggplot")

# Function to plot ventilation age
def plot_ventilation_age(lat, zt, dage, title, filename):
    plt.fill_between(lat, zt.min(), zt.max(), color='#695447')
    contour_filled = plt.contourf(lat, zt, dage, cmap=cm.dense)
    contour_lines = plt.contour(lat, zt, dage, colors='k', linewidths=0.5)
    plt.xlabel("Latitude [°N]", fontsize=16)
    plt.ylabel("Depth [m]", fontsize=16)
    cbar = plt.colorbar(contour_filled)
    cbar.set_label(r"Ventilation age (years)", fontsize=16)
    plt.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.1f')
    plt.gca().invert_yaxis()
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=600)
    plt.show()

# Function to perform statistical tests and print results
def perform_statistical_tests(open_dage, close_dage):
    statistic_mw, p_value_mw = mannwhitneyu(open_dage, close_dage)
    statistic_ks, p_value_ks = ks_2samp(open_dage, close_dage)

    # Interpretation of tests
    print(f'Mann-Whitney U test statistic: {round(statistic_mw, 3)}')
    print(f'Mann-Whitney U test p-value: {round(p_value_mw, 3)}')
    print(f'KS test statistic: {round(statistic_ks, 3)}')
    print(f'KS test p-value: {round(p_value_ks, 3)}')

    if p_value_mw < 0.05:
        print('Significant difference between distributions (Mann-Whitney U test).')
    else:
        print('No significant difference between distributions (Mann-Whitney U test).')

    if p_value_ks < 0.05:
        print('Significant difference between distributions (KS test).')
    else:
        print('No significant difference between distributions (KS test).')

# Function to plot ECDFs
def plot_ecdfs(open_dage, close_dage):
    def ecdf(data):
        sorted_data = np.sort(data)
        n = len(data)
        y = np.arange(1, n + 1) / n
        return sorted_data, y

    x1, y1 = ecdf(open_dage)
    x2, y2 = ecdf(close_dage)

    plt.plot(x1, y1, label='Open')
    plt.plot(x2, y2, label='Closed')
    plt.xlabel('Ventilation age (years)', fontsize=16)
    plt.ylabel('ECDFs', fontsize=16)
    plt.legend()
    plt.tight_layout();
    plt.savefig("../figs/fig4f.png", dpi=600);

if __name__ == "__main__":
    # Load datasets
    ds_open = xr.open_dataset("../data/open/fields_biogem_3d.nc")
    ds_close = xr.open_dataset("../data/closed/fields_biogem_3d.nc")

    # Extract data
    zt_open = ds_open["zt"].to_numpy()
    lat_open = ds_open["lat"].to_numpy()
    dage_open = ds_open["misc_col_Dage"].isel(time=0).mean(dim="lon")

    zt_close = ds_close["zt"].to_numpy()
    lat_close = ds_close["lat"].to_numpy()
    dage_close = ds_close["misc_col_Dage"].isel(time=0).mean(dim="lon")

    dage_anom = (dage_close - dage_open)

    # Plot ventilation age for open case
    plot_ventilation_age(lat_open, zt_open, dage_open, "Ventilation Age (Open Case)", "../figs/fig4a.png")

    # Plot ventilation age for closed case
    plot_ventilation_age(lat_close, zt_close, dage_close, "Ventilation Age (Closed Case)", "../figs/fig4b.png")

    # Data processing and visualization for comparison
    open_dage = dage_open.flatten()
    close_dage = dage_close.flatten()

    open_dage = open_dage[~np.isnan(open_dage)]
    close_dage = close_dage[~np.isnan(close_dage)]

    # KDE plot
    sns.kdeplot(open_dage, label='Open', fill=False);
    sns.kdeplot(close_dage, label='Closed', fill=False);
    plt.xlabel(r"Ventilation age (years)", fontsize=16);
    plt.ylabel('Probability Density', fontsize=16);
    plt.legend();
    plt.tight_layout();
    plt.savefig("../figs/fig4e.png", dpi=600);

    # Box plot
    combined_data = np.concatenate([open_dage, close_dage])
    grouping_array = np.concatenate([['Open'] * len(open_dage), ['Closed'] * len(close_dage)])
    sns.boxplot(x=grouping_array, y=combined_data);
    plt.ylabel(r"Ventilation age (years)", fontsize=16);
    plt.tight_layout();
    plt.savefig("../figs/fig4d.png", dpi=600);

    # Perform statistical tests
    perform_statistical_tests(open_dage, close_dage)

    # Plot ECDFs
    plot_ecdfs(open_dage, close_dage)
