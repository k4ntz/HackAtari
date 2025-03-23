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
    if all_logs == []:
        return

    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    
    # Prepare data and calculate statistics
    data = []
    for log in all_logs:
        label = log.run_label or "None"
        if log.times and isinstance(log.times[0], (list, np.ndarray)):
            flattened_times = [t for episode in log.times for t in episode]
        else:
            flattened_times = log.times
        
        data.extend([{"Modification": label, "Duration": t} for t in flattened_times])
    
    df = pd.DataFrame(data)
    
    # Calculate summary statistics with precision handling
    stats = df.groupby('Modification')['Duration'].agg(
        ['mean', 'median', 'std', 'min', 'max', 'count']
    ).reset_index()
    
    # Dynamic decimal formatting based on values
    def format_duration(x):
        if abs(x) < 0.001:
            return "≈0"
        if abs(x) < 1:
            return f"{x:.4f}"
        return f"{x:.2f}"

    # Apply formatting only to numeric columns
    for col in stats.columns:
        if pd.api.types.is_numeric_dtype(stats[col]):
            stats[col] = stats[col].apply(format_duration)
        elif col == 'Modification':  # Handle categorical ordering
            stats[col] = stats[col].astype('category').cat.set_categories(unique_mods)
    
    stats.columns = [
        'Modification', 'Mean', 'Median', 'Std Dev', 
        'Minimum', 'Maximum', 'Episode Count'
    ]
    
    # Order stats according to unique_mods
    stats['Modification'] = pd.Categorical(
        stats['Modification'], 
        categories=unique_mods, 
        ordered=True
    )
    stats = stats.sort_values('Modification')

    # Generate and display Markdown analysis
    markdown_text = f"""
### Episode Duration Analysis

This plot complements reward metrics by showing temporal efficiency across modifications. The boxplots reveal:

- **Median duration**: Typical episode length for each configuration
- **Time consistency**: Spread indicates stability of episode durations
- **Timeout patterns**: Right-side outliers show particularly long episodes

**Key Statistics:**

{stats.to_markdown(index=False)}

"""
    display(Markdown(markdown_text))

    # Create the plot with adjusted scale if needed
    plt.figure(figsize=STYLE["tall_figure_size"])
    if df['Duration'].max() > 0:
        ax = sns.boxplot(
            data=df,
            y="Modification",
            x="Duration",
            order=unique_mods,
            hue_order=unique_mods,
            palette=palette,
            width=0.6,
            linewidth=1.5,
            hue="Modification",
            flierprops=STYLE["flierprops"]
        )
        plt.xlabel("Duration (seconds)", fontsize=STYLE["axis_label_fontsize"])
    else:
        plt.text(0.5, 0.5, 'No duration data available', 
                ha='center', va='center', fontsize=12)
    
    plt.title("Episode Duration Distribution", fontsize=STYLE["title_fontsize"])
    plt.ylabel("")
    plt.grid(**STYLE["grid"])
    plt.tight_layout()
    plt.show()


######## Not used ###########

def plot_time_distribution(all_logs: List[LogData]) -> None:
    """Plot time distribution with list-of-lists handling"""
    if all_logs == []:
        return

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
