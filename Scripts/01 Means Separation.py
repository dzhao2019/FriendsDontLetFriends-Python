'''
title: "01 Means Separation"
author: "Dandan Zhao"
date: "7/30/2024"
output: png figure
'''

# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, wilcoxon, ks_2samp

# Set the random seed for reproducibility
np.random.seed(666)

# Generate the data
# group1: Normally distributed data with mean = 1 and standard deviation = 1
group1 = np.random.normal(loc=1, scale=1, size=100)

# group2: Log-normally distributed data
# The log-normal distribution parameters are derived from the normal distribution parameters
group2 = np.random.lognormal(mean=np.log(1**2 / np.sqrt(1**2 + 1**2)),
                             sigma=np.sqrt(np.log(1 + (1**2 / 1**2))),
                             size=100)

# Calculate and print basic statistics
print("Standard deviation of group1:", np.std(group1))
print("Standard deviation of group2:", np.std(group2))
print("Mean of group1:", np.mean(group1))
print("Mean of group2:", np.mean(group2))
print("Median of group1:", np.median(group1))
print("Median of group2:", np.median(group2))
print("IQR of group1:", np.percentile(group1, 75) - np.percentile(group1, 25))
print("IQR of group2:", np.percentile(group2, 75) - np.percentile(group2, 25))

# Combine the data into a long format dataframe
# This is useful for plotting with seaborn
groups_long = pd.DataFrame({
    'group1': group1,
    'group2': group2
}).melt(var_name='group', value_name='response')

# Output the dataframe to a TSV file
groups_long.to_csv("01_data_groups_long.tsv", sep='\t', index=False)

# Perform statistical tests
# t-test: Compares the means of two groups
t_test_p = ttest_ind(group1, group2).pvalue

# Wilcoxon rank-sum test: Compares the medians of two groups
wilcox_p = wilcoxon(group1, group2).pvalue

# Kolmogorov-Smirnov test: Compares the distributions of two groups
ks_p = ks_2samp(group1, group2).pvalue

# Print the p-values of the tests
print("t-test p-value:", t_test_p)
print("Wilcoxon test p-value:", wilcox_p)
print("KS test p-value:", ks_p)

# Set the seaborn style for the plots
sns.set(style="white")
sns.set_style("ticks", {"xtick.major.size": 16, "ytick.major.size": 16})
sns.despine(top=False, right=False)  # Keep the top and right spines

# Set the seaborn style for the plots
sns.set(style="white")
sns.set_style("ticks", {"xtick.major.size": 16, "ytick.major.size": 16})
sns.despine(top=True, right=True)  # Keep the top and right spines

# Define pastel color palette
pastel_palette = sns.color_palette("pastel")
# Choose green and purple from pastel palette
custom_palette = {"group1": pastel_palette[2], "group2": pastel_palette[3]}

# Create subplots
fig, axes = plt.subplots(1, 3, figsize=(12, 5), sharey=False)

# Bar plot
sns.barplot(
    x="group", y="response", hue="group", data=groups_long,
    errorbar="sd", palette=custom_palette, alpha=0.8, ax=axes[0], dodge=False,
)
axes[0].spines['right'].set_visible(False)
axes[0].spines['top'].set_visible(False)
axes[0].tick_params(axis='y', labelsize=16)
axes[0].yaxis.get_offset_text().set_fontsize(16)
axes[0].set_xticklabels(['group1','group2'], fontsize=16)
axes[0].set_title(
    f"group1: mean = {np.mean(group1):.2f}; sd = {np.std(group1):.2f}\n"
    f"group2: mean = {np.mean(group2):.2f}; sd = {np.std(group2):.2f}\n" , fontsize=14
)
axes[0].set_xlabel("Group", fontsize=16)
axes[0].set_ylabel("Response", fontsize=16)
axes[0].legend().set_visible(False)
axes[0].text(0.5, -0.25, f"They are the same!\nP = {t_test_p:.2g} (t-test)", ha='center',
             va='center', transform=axes[0].transAxes, fontsize=14)
# Change the error bar color and width
for artist in axes[0].lines:
    artist.set_color('gray')
    artist.set_linewidth(1)

# Box plot
sns.boxplot(
    x="group", y="response", hue="group", data=groups_long,
    palette=custom_palette, ax=axes[1], dodge=False
)
axes[1].spines['right'].set_visible(False)
axes[1].spines['top'].set_visible(False)
axes[1].tick_params(axis='y', labelsize=16)
axes[1].yaxis.get_offset_text().set_fontsize(16)
axes[1].set_xticklabels(['group1','group2'], fontsize=16)
axes[1].set_title(
    f"group1: median = {np.median(group1):.2f}; IQR = {np.percentile(group1, 75) - np.percentile(group1, 25):.2f}\n"
    f"group2: median = {np.median(group2):.2f}; IQR = {np.percentile(group2, 75) - np.percentile(group2, 25):.2f}\n"
    , fontsize=14
)
axes[1].set_xlabel("Group", fontsize=16)
axes[1].set_ylabel("Response", fontsize=16)
axes[1].legend().set_visible(False)
axes[1].text(0.5, -0.25, f"Hmmmmm...\nP = {wilcox_p:.2g} (Wilcoxon rank sum test)", ha='center',
             va='center', transform=axes[1].transAxes, fontsize=14)


# Swarm plot
sns.swarmplot(
    x="group", y="response", hue="group", data=groups_long, dodge=True,
    alpha=0.8, size=5, palette=custom_palette, ax=axes[2]
)
axes[2].spines['right'].set_visible(False)
axes[2].spines['top'].set_visible(False)
axes[2].tick_params(axis='y', labelsize=16)
axes[2].yaxis.get_offset_text().set_fontsize(16)
axes[2].set_xticklabels(['group1','group2'], fontsize=16)
axes[2].set_title(
    f"group1: median = {np.median(group1):.2f}; IQR = {np.percentile(group1, 75) - np.percentile(group1, 25):.2f}\n"
    f"group2: median = {np.median(group2):.2f}; IQR = {np.percentile(group2, 75) - np.percentile(group2, 25):.2f}\n"
    , fontsize=14
)
axes[2].set_xlabel("Group", fontsize=16)
axes[2].set_ylabel("Response", fontsize=16)
axes[2].legend().set_visible(False)
axes[2].text(0.5, -0.25, f"OH!!!\nP = {ks_p:.2g} (Kolmogorov–Smirnov test)", ha='center',
             va='center', transform=axes[2].transAxes, fontsize=14)

plt.tight_layout()
plt.show()

# Save the plots as PNG files
fig.savefig("01_Mean_separation_plots.png")


