from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display
from typing import List
from matplotlib.colors import LogNorm, ListedColormap
from matplotlib.ticker import LogFormatterMathtext
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, ListedColormap
from matplotlib.ticker import LogFormatterMathtext
import pandas as pd
import seaborn as sns   
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from automatic_evaluator.log_data import LogData
from automatic_evaluator.plots.style import STYLE

def _get_sorted_modifications(all_logs: List[LogData]) -> List[str]:
    """Helper to sort modifications with 'None' first, then others alphabetically."""
    unique_mods = {log.run_label for log in all_logs}
    sorted_mods = []
    if 'None' in unique_mods:
        sorted_mods.append('None')
        remaining = sorted([mod for mod in unique_mods if mod != 'None'], key=lambda x: x.lower())
        sorted_mods.extend(remaining)
    else:
        sorted_mods = sorted(unique_mods, key=lambda x: x.lower())
    return sorted_mods



def plot_time_boxplot(all_logs: List[LogData]) -> None:
    """Plot time distribution comparison with list data handling"""
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    
    # Prepare data
    data = []
    for log in all_logs:
        label = log.run_label or "None"
        # Flatten nested time lists if necessary
        if log.times and isinstance(log.times[0], (list, np.ndarray)):
            flattened_times = [t for episode in log.times for t in episode]
        else:
            flattened_times = log.times
        
        data.extend([{"Modification": label, "Duration": t} for t in flattened_times])
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=STYLE["tall_figure_size"])

    sns.boxplot(
        data=df,
        y="Modification",
        x="Duration",
        order=unique_mods,
        palette=palette,
        width=0.6,
        linewidth=1.5,
        hue="Modification",
        flierprops=STYLE["flierprops"]
    )
    
    plt.title("Episode Duration Distribution", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Duration (seconds)", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("")
    plt.grid(**STYLE["grid"])
    plt.tight_layout()
    plt.show()



######## Not used ###########

def plot_time_distribution(all_logs: List[LogData]) -> None:
    """Plot time distribution with list-of-lists handling"""
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    
    data = []
    for log in all_logs:
        label = log.run_label or "None"
        # Handle list of lists
        if log.times and isinstance(log.times[0], (list, np.ndarray)):
            for episode_times in log.times:
                data.extend([{"Modification": label, "Duration": t} for t in episode_times])
        else:
            data.extend([{"Modification": label, "Duration": t} for t in log.times])
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=STYLE["figure_size"])
    
    sns.kdeplot(
        data=df,
        x="Duration",
        hue="Modification",
        hue_order=unique_mods,
        palette=palette,
        common_norm=False,
        linewidth=2
    )
    
    plt.title("Episode Duration Distribution by Modification", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Duration (seconds)", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("Density", fontsize=STYLE["axis_label_fontsize"])
    plt.grid(**STYLE["grid"])
    plt.legend(title="Modifications", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()