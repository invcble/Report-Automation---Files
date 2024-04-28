import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


dat_long = pd.read_csv('MerckCombined.csv')

# Separate scores from ranges and convert scores to numeric
dat_long[['Score', 'range']] = dat_long['Score'].str.split(' ', expand=True)
dat_long['Score'] = dat_long['Score'].astype(float)
dat_long['range'] = dat_long['range'].fillna(' ')
dat_long['label'] = dat_long['Score'].astype(str) + ' ' + dat_long['range']

# Filter data based on ScaleID
s = 1

dat_long_filtered = dat_long[dat_long['ScaleID'] == f'MOTAI{s}']
positions = np.arange(len(dat_long_filtered))
print(dat_long_filtered)

fig, ax = plt.subplots(figsize=(10, 6))

background_bars = ax.bar(x=positions + 0.02, height=dat_long_filtered['Score'] + 0.1, width=0.9, color='#cccccc', alpha=0.5, label='Background')
main_bars = ax.bar(dat_long_filtered['Scale'], dat_long_filtered['Score'], width=0.9, color=['#58a7ea', '#65efdb'], alpha=1, label='Main')

for pos, score, score_range in zip(positions, dat_long_filtered['Score'], dat_long_filtered['range']):
    ax.text(pos, 0.5, f"{score} {score_range}", color='black', ha="center", fontsize=12)

# Setting y-axis
ax.set_ylim(0, 7)
ax.set_yticks(np.arange(0, 8, 1))

# Removing x-axis labels
ax.set_xticklabels([])
ax.set_xticks(positions)
ax.tick_params(axis='both', which='both', length=0)

# Set grid and other aesthetics
ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, color='grey')
ax.set_axisbelow(True)

# Remove unnecessary spines and ticks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
