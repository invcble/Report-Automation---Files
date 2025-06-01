import matplotlib.pyplot as plt
import numpy as np

################################################################################################

def get_name(dataframe, s):
    newdf = dataframe[dataframe['ScaleID'] == 'MOTAI'+f'{s}']
    return newdf['FName'].values[0][0] + '. ' + newdf['LName'].values[0].capitalize()

################################################################################################

def create_chart(dataframe, scale_id, save_path, mode):
    dat_long_filtered = dataframe[dataframe['ScaleID'] == scale_id]    
    positions = np.arange(len(dat_long_filtered))
    # print(dat_long_filtered)

    fig, ax = plt.subplots(figsize=(10, 6))
    h_adj = 0.03
    Fontsize = 25

    if mode == 1:
        h_adj = 0.2
        Fontsize = 30
        Color = ['#58a7ea', '#65efdb']
    elif mode == 2:
        Color = ['#58a7ea', '#65efdb', '#64CA55', '#EFCD5B']
    elif mode == 3:
        Color = ['#58a7ea', '#65efdb', '#EFCD5B']
    else:
        raise Exception("Only 1, 2 or 3 is accepted as mode.")
    
    ax.bar(x=positions + 0.04, height=dat_long_filtered['Score'] + h_adj, width=0.9, color='#cccccc', alpha=0.5, label='Background')
    ax.bar(dat_long_filtered['Scale'], dat_long_filtered['Score'], width=0.9, color=Color, alpha=1, label='Main')

    for pos, score, score_range in zip(positions, dat_long_filtered['Score'], dat_long_filtered['range']):
        if score > 0:
            if score_range != ' ':
                if score_range == "[Inf--Inf]":
                    max = int(np.ceil(score))
                    min = int(np.floor(score))
                else:
                    max = int(score_range[1:-1].split("-")[1])
                    min = int(score_range[1:-1].split("-")[0])
                    if max < score:
                        max = int(np.ceil(score))
                    if min > score:
                        min = int(np.floor(score))
                ax.text(pos, 0.7, f"{round(score, 2)}\n[{min}-{max}]", color='black', ha="center", fontsize=Fontsize)
            else:
                ax.text(pos, 0.7, f"{round(score, 2)}\n{score_range}", color='black', ha="center", fontsize=Fontsize)
        else:
            ax.text(pos, 0.7, f"NA", color='black', ha="center", fontsize=Fontsize)
    
    ax.set_ylim(0, 7)
    ax.set_yticks(np.arange(0, 8, 1))
    ax.tick_params(axis='y', labelsize=20)
    ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, color='grey')
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticklabels([])
    ax.set_xticks(positions)
    ax.tick_params(axis='both', which='both', length=0)

    fig.savefig(save_path + scale_id + '.png', dpi=100, bbox_inches='tight')
    plt.close(fig)