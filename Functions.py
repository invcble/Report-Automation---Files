import matplotlib.pyplot as plt
import numpy as np

################################################################################################

def create_chart(dataframe, scale_id, save_path):
    # Filter the dataframe based on the scale ID
    dat_long_filtered = dataframe[dataframe['ScaleID'] == scale_id]
    print(dat_long_filtered)
    positions = np.arange(len(dat_long_filtered))

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(5, 3))

    # Create background and main bars
    ax.bar(x=positions + 0.04, height=dat_long_filtered['Score'] + 0.2, width=0.9, color='#cccccc', alpha=0.5, label='Background')
    ax.bar(dat_long_filtered['Scale'], dat_long_filtered['Score'], width=0.9, color=['#58a7ea', '#65efdb'], alpha=1, label='Main')

    # Add text labels above bars
    for pos, score, score_range in zip(positions, dat_long_filtered['Score'], dat_long_filtered['range']):
        ax.text(pos, 0.7, f"{score} {score_range}", color='black', ha="center", fontsize=12)

    # Set y-axis limits and ticks
    ax.set_ylim(0, 7)
    ax.set_yticks(np.arange(0, 8, 1))

    # Set grid and other aesthetics
    ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, color='grey')
    ax.set_axisbelow(True)

    # Remove unnecessary spines and ticks
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Hide x-axis tick labels (if necessary)
    ax.set_xticklabels([])
    ax.set_xticks(positions)
    ax.tick_params(axis='both', which='both', length=0)

    # Save the figure
    fig.savefig(save_path + scale_id + '.png', dpi=100, bbox_inches='tight')

    # Close the figure to prevent display in interactive environments
    plt.close(fig)