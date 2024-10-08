"""
Title: Bar_plots_for_means_separation
Author: dzhao
Date: 5/1/2024
Description: This script generates a series of plots (bar plot, box plot, and dot plot)
to analyze and compare two groups sampled from different distributions.

Requirements:
- Python packages: numpy, pandas, matplotlib, seaborn, scipy
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, wilcoxon, ks_2samp

# Set seed for reproducibility
np.random.seed(666)

# Set seaborn styles
sns.set(style="white")
sns.set_style("ticks", {"xtick.major.size": 16, "ytick.major.size": 16})
sns.despine(top=True, right=True)

# Data generation
group1 = np.random.normal(loc=0.93, scale=1, size=100)
group2 = np.random.normal(loc=0.98, scale=0.93, size=100)

# Create DataFrame in long format for Seaborn
groups_long = pd.DataFrame({
    'group1': group1,
    'group2': group2
}).melt(var_name='group', value_name='response')

# Statistical Tests
t_result = ttest_ind(group1, group2)
wilcox_result = wilcoxon(group1, group2)
ks_result = ks_2samp(group1, group2)

# Create the figure and axes
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# Color palette matching the provided plot
custom_palette = ["#99D599", "#CBBEDC"]

# Bar plot
sns.barplot(data=groups_long, x='group', y='response', errorbar='sd', palette=custom_palette, ax=axes[0])
axes[0].set_title(f'They are the same!\nP = {t_result.pvalue:.2f} (t-test)', fontsize=14, fontweight='bold')
axes[0].set_xlabel("Group", fontsize=12)
axes[0].set_ylabel("Response", fontsize=12)
axes[0].text(0.5, -0.25, "group1: mean = 0.93; sd = 1\ngroup2: mean = 0.98; sd = 0.93",
             ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[0].transAxes)
sns.despine(ax=axes[0], top=True, right=True)

# Box plot
sns.boxplot(data=groups_long, x='group', y='response', palette=custom_palette, ax=axes[1])
axes[1].set_title(f'Hmmmmm...\nP = {wilcox_result.pvalue:.2f} (Wilcoxon rank sum test)', fontsize=14, fontweight='bold')
axes[1].set_xlabel("Group", fontsize=12)
axes[1].set_ylabel("Response", fontsize=12)
axes[1].text(0.5, -0.25, "group1: median = 0.95; IQR = 1.5\ngroup2: median = 0.62; IQR = 1",
             ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[1].transAxes)
sns.despine(ax=axes[1], top=True, right=True)

# Dot (swarm) plot
sns.swarmplot(data=groups_long, x='group', y='response', hue='group', palette=custom_palette, ax=axes[2], size=6)
axes[2].set_title(f'OH!!!\nP = {ks_result.pvalue:.3f} (KS-test)', fontsize=14, fontweight='bold')
axes[2].set_xlabel("Group", fontsize=12)
axes[2].set_ylabel("Response", fontsize=12)
axes[2].text(0.5, -0.25, "group1: median = 0.95; IQR = 1.5\ngroup2: median = 0.62; IQR = 1",
             ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[2].transAxes)
sns.despine(ax=axes[2], top=True, right=True)
axes[2].legend([],[], frameon=False)  # Hide the legend

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()

# Save the combined plot as PNG and SVG files
fig.savefig("01_dont_bar_plot.png", dpi=300)
fig.savefig("01_dont_bar_plot.svg", format='svg')
