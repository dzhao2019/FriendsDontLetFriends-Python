"""
Title: Violin_plot_for_small_n
Author: dzhao
Date: 8/1/2024
Description: This script generates a series of plots (violin plot, box plot, and dot plot)
to demonstrate how unreliable distribution and quartile measures are with small sample sizes (n=5).

Requirements:
- Python packages: numpy, pandas, matplotlib, seaborn, statsmodels, scipy
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

# Set the random seed for reproducibility
np.random.seed(666)

# Generate three sets of data from a normal distribution with mean = 1 and sd = 1
data = {'group1': [0.682, -0.2479, 3.019, 1.79, 3.022],
        'group2': [-0.890, 1.119, 0.156, 1.6405, -0.423],
        'group3': [1.8088, 3.068, 1.9782, -0.816, -0.8012]}

data_set = pd.DataFrame(data)
data_set = data_set.melt(var_name='Group', value_name='Response')

# Set the seaborn style
sns.set(style="white")
sns.set_style("ticks", {"xtick.major.size": 16, "ytick.major.size": 16})

# Combine plots
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# Color palette to match the provided image
custom_palette = ["#99D599", "#CBBEDC", "#FBCEA0"]

# Violin plot with median points
sns.violinplot(x="Group", y="Response", data=data_set, palette=custom_palette, alpha=0.8, inner=None, ax=axes[0])
sns.pointplot(x="Group", y="Response", data=data_set, join=False, color='black', markers='.', ci=None, estimator=np.median, ax=axes[0])
axes[0].set_title("Points are median.", fontsize=14, fontweight='bold')
axes[0].set_xlabel("Group", fontsize=12)
axes[0].set_ylabel("Response", fontsize=12)
axes[0].text(0.5, -0.25, "The distributions are different!\nI wonder what's going on.", ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[0].transAxes)
sns.despine(ax=axes[0], top=True, right=True)  # Apply sns.despine() to the first plot

# Box plot with transparency adjustment
sns.boxplot(x="Group", y="Response", data=data_set, palette=custom_palette, ax=axes[1])
# Manually set transparency for the boxes
for patch in axes[1].artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0.8))  # Set alpha to 0.8
axes[1].set_title("Boxes span IQR.", fontsize=14, fontweight='bold')
axes[1].set_xlabel("Group", fontsize=12)
axes[1].set_ylabel("Response", fontsize=12)
axes[1].text(0.5, -0.25, "The quartiles are different!\nI wonder what's going on.", ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[1].transAxes)
sns.despine(ax=axes[1], top=True, right=True)  # Apply sns.despine() to the second plot

# Strip plot with jitter and color matching
sns.stripplot(x="Group", y="Response", data=data_set, palette=custom_palette, alpha=0.8, jitter=True, size=10, ax=axes[2])
axes[2].set_title("n = 5", fontsize=14, fontweight='bold')
axes[2].set_xlabel("Group", fontsize=12)
axes[2].set_ylabel("Response", fontsize=12)
axes[2].text(0.5, -0.25, "Never mind...\nToo little data to say anything.", ha="center", fontsize=12, color='black', fontweight='bold', transform=axes[2].transAxes)
sns.despine(ax=axes[2], top=True, right=True)  # Apply sns.despine() to the third plot

# Adjust layout for better display
plt.tight_layout()

# Show the plot
plt.show()

# Save the combined plot as PNG and SVG files
fig.savefig("../02.Beware_of_small_n_box_violin_plot.png", dpi=300)
fig.savefig("../02.Beware_of_small_n_box_violin_plot.svg", format='svg')
