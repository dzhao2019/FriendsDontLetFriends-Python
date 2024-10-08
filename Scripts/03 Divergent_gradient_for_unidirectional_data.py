"""
Title: Divergent Gradient for Unidirectional Data Visualization
Author: dzhao
Date: 8/10/2024
Description: This script generates a set of scatter plots to demonstrate good and bad uses of color gradients for data visualization. It highlights how gradient color mappings should and should not be applied to unidirectional data.

Requirements:
- Python packages: numpy, pandas, matplotlib, seaborn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm

# Set seaborn style for the plots
sns.set(style="whitegrid")
sns.set_style("ticks", {"xtick.major.size": 16, "ytick.major.size": 16})
sns.despine(top=True, right=True)

# Data Simulation
np.random.seed(666)
Dir1 = pd.DataFrame({
    "FPKM": [5, 10, 20, 40, 60, 80, 100, 120],
    "Gene": range(1, 9)
})

Dir2 = pd.DataFrame({
    "log2FC": [-10, -4, -2, 0, 2, 4, 10],
    "Gene": range(1, 8)
})

Dir3 = pd.DataFrame({
    "z.score": [-2.5, -2, -1, 0, 1, 2, 2.5],
    "Gene": range(1, 8)
})

# Setup Matplotlib Figure
fig, axes = plt.subplots(2, 2, figsize=(9, 7))

# Color mappings
cmaps = {
    'viridis': cm.get_cmap('viridis', 256),
    'RdBu': cm.get_cmap('RdBu_r', 256),
    'YlGnBu': cm.get_cmap('YlGnBu', 256)
}

# Function to create scatter plots with color bar and hlines
def create_plot(ax, data, x, y, cmap, title, caption):
    # Scatter plot
    sc = ax.scatter(data[x], data[y], c=data[x], cmap=cmap, edgecolor='grey', s=100)
    for _, row in data.iterrows():
        ax.hlines(y=row[y], xmin=0, xmax=row[x], color='grey', linewidth=1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axvline(0, color='grey', linewidth=1)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('Gene', fontsize=12)
    ax.set_xlabel(x, fontsize=12)
    ax.grid(True, which='both', linestyle='-', linewidth=0.5)
    ax.set_yticks([])

    # Adding color bar
    norm = plt.Normalize(vmin=data[x].min(), vmax=data[x].max())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical')

    # Caption
    ax.text(0.5, -0.25, caption, transform=ax.transAxes, ha='center', va='top', fontsize=11, color='black')

# Define datasets, titles, captions
datasets = [(Dir1, 'FPKM'), (Dir2, 'log2FC'), (Dir3, 'z.score'), (Dir1, 'FPKM')]
titles = [
    "Darkest color = Min\nLightest color = Max",
    "Lightest color = 0\nDarkest colors = Max absolutes",
    "Darkest color = Max\nLightest color = Min",
    "Lightest color means nothing\n(neither mean nor median)."
]
captions = ["This is good.", "This is good.", "This is good.", "A data visualization sin"]
cmap_keys = ['viridis', 'RdBu', 'YlGnBu', 'RdBu']

# Generate plots
for ax, ((data, y), title, caption, cmap_key) in zip(axes.flatten(), zip(datasets, titles, captions, cmap_keys)):
    cmap = cmaps[cmap_key]
    create_plot(ax, data, y, 'Gene', cmap, title, caption)

# Adjust layout for better display
plt.tight_layout()

# Show the plot
plt.show()

# Save the plot
fig.savefig("03_Divergent_gradient_for_unidirectional_data.png", dpi=300)
fig.savefig("03_Divergent_gradient_for_unidirectional_data.svg", format='svg')
