

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

def plot_action_reward_correlation(all_logs: List[LogData], selected_game: str):
    """
    Plot correlation heatmaps with multi-row layout and parallel colorbar
    """
    # Add action-reward correlation Markdown
    markdown_text = f"""
### Action-Reward Relationship Analysis

This visualization reveals how often specific actions led to particular reward values. Key insights:

- **Common combinations**: Bright areas show frequent action-reward pairs
- **Ineffective actions**: Dark gray areas indicate never-seen combinations
- **Reward consistency**: Vertical patterns show actions with predictable outcomes
- **Modification differences**: Compare how environment changes affect reward distributions

_Color intensity shows occurrence frequency (log scale), annotations show exact counts._
"""
    display(Markdown(markdown_text))

    # Calculate layout dimensions
    n_mods = len(all_logs)
    ncols = min(2, n_mods)  # Max 3 per row
    nrows = (n_mods + ncols - 1) // ncols
    
    # Create figure with dynamic sizing
    fig = plt.figure(figsize=(4*ncols + 1, 3*nrows + 1))
    fig.suptitle(f"Action-Reward Correlation: {selected_game}\n", fontsize=14, y=0.95)
    
    # Create grid specification
    gs = fig.add_gridspec(nrows, ncols + 1, width_ratios=[1]*ncols + [0.1])
    
    # Create common bins
    all_rewards = [r for log in all_logs for ep in log.rewards for r in ep]
    reward_bins = np.linspace(min(all_rewards), max(all_rewards), 10)
    
    
    # Find maximum count for logarithmic scale
    max_count = 0
    for log in all_logs:
        actions = [a for ep in log.actions for a in ep]
        rewards = [r for ep in log.rewards for r in ep]
        hist, _, _ = np.histogram2d(rewards, actions, bins=[reward_bins, np.unique(actions)])
        current_max = hist.max()
        if current_max > max_count:
            max_count = current_max

    
    # Create logarithmic bins starting from 1
    max_count = max(1, max_count)  # Ensure minimum range
    log_bins = np.logspace(0, np.log10(max_count), num=10)
    log_ticks = [10**i for i in range(0, int(np.log10(max_count)) + 2)]
    bins = [0] + list(log_bins)  # Separate zero bin

    # Create discrete colormap
    cmap = plt.get_cmap('viridis')
    norm = LogNorm(vmin=1, vmax=10**np.ceil(np.log10(max_count)))

    new_colors = cmap(np.linspace(0, 1, 256))
    new_colors = np.vstack(([0.15, 0.15, 0.15, 1], new_colors))  # Dark gray for zeros
    cmap_zero = ListedColormap(new_colors)

    # Calculate logarithmic normalization (start from 1)
    max_non_zero = max(1, max_count)
    norm = LogNorm(vmin=1, vmax=10**np.ceil(np.log10(max_non_zero)))
    
    # Plot each modification
    axes = []
    for idx, log in enumerate(all_logs):
        row = idx // ncols
        col = idx % ncols
        ax = fig.add_subplot(gs[row, col])
        axes.append(ax)
        
        # Flatten data
        actions = [a for ep in log.actions for a in ep]
        rewards = [r for ep in log.rewards for r in ep]
        unique_actions = np.unique(actions)
        action_edges = np.arange(min(unique_actions)-0.5, max(unique_actions)+1.5, 1)
        
        # Create histogram
        hist, x_edges, y_edges = np.histogram2d(
            rewards, actions, 
            bins=[reward_bins, action_edges]
        )

        # Create masked array for zeros
        hist_masked = np.ma.masked_where(hist == 0, hist)
        
        # Plot heatmap with two layers
        ax.pcolormesh(  # Base layer for zeros
            x_edges, y_edges, hist.T,
            cmap=ListedColormap(['#262626']),
            vmin=0,
            vmax=1
        )
        im = ax.pcolormesh(  # Top layer for non-zero values
            x_edges, y_edges, hist_masked.T,
            cmap=cmap_zero,
            norm=norm,
            shading='auto'
        )

        

        # Add annotations and labels
        y_centers = (y_edges[:-1] + y_edges[1:]) / 2
        ax.set_yticks(y_centers)
        ax.set_yticklabels(unique_actions)
        ax.set_title(log.run_label.replace("\n", " - "), fontsize=10)
        
        # Add text annotations only for non-zero values
        for i in range(hist.shape[0]):
            for j in range(hist.shape[1]):
                count = hist[i, j]
                if count > 0:  # Skip zeros
                    ax.text(
                        (x_edges[i] + x_edges[i+1])/2,
                        (y_edges[j] + y_edges[j+1])/2,
                        f"{int(count)}",
                        ha='center', va='center',
                        color='white' if count < max_non_zero**0.3 else 'black',
                        fontsize=8
                    )
                
        
        # Only label outer axes
        if col == 0:
            ax.set_ylabel("Action")
        if row == nrows-1:
            ax.set_xlabel("Reward Value")
    
    # Create colorbar with filtered ticks
    # Create formatted colorbar
    # Create colorbar for non-zero values
    cax = fig.add_subplot(gs[:, -1])
    cbar = fig.colorbar(im, cax=cax, format=LogFormatterMathtext(labelOnlyBase=False))
    cbar.set_ticks([10**i for i in range(0, int(np.log10(max_non_zero)) + 2)])
    cbar.set_label("Frequency (log scale)\n(excluding zeros)", rotation=270, labelpad=25)
    
    # Adjust spacing
    plt.tight_layout()
    plt.subplots_adjust(
        right=0.85,
        hspace=0.4,
        wspace=0.3
    )
    
    plt.show()


def plot_reward_vs_time(all_logs: List[LogData]) -> None:
    """Plot reward vs time correlation with statistical analysis"""
    if not all_logs:
        return

    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    # Prepare data and calculate statistics
    stats_data = []
    plot_data = []

    for mod in unique_mods:
        mod_rewards = []
        mod_times = []
        
        for log in all_logs:
            if log.run_label == mod:
                # Process rewards and times
                rewards = log.epoch_rewards
                times = log.times
                
                if rewards and isinstance(rewards[0], (list, np.ndarray)):
                    rewards = [sum(ep) for ep in rewards]
                if times and isinstance(times[0], (list, np.ndarray)):
                    times = [sum(ep) for ep in times]
                
                min_length = min(len(rewards), len(times))
                mod_rewards.extend(rewards[:min_length])
                mod_times.extend(times[:min_length])
        
        if mod_rewards and mod_times:
            # Calculate statistics
            mean_reward = np.mean(mod_rewards)
            mean_time = np.mean(mod_times)
            try:
                corr_coef = np.corrcoef(mod_rewards, mod_times)[0,1]
            except:
                corr_coef = np.nan
                
            stats_data.append({
                'Modification': mod,
                'Episodes': len(mod_rewards),
                'Mean Reward': mean_reward,
                'Mean Duration': mean_time,
                'R-Time Correlation': corr_coef
            })
            
            # Store for plotting
            plot_data.extend([
                {'Modification': mod, 'Reward': r, 'Duration': t}
                for r, t in zip(mod_rewards, mod_times)
            ])

    # Create and format stats table
    stats_df = pd.DataFrame(stats_data)
    stats_df = stats_df.round(3)
    stats_df['Mean Duration'] = stats_df['Mean Duration'].apply(
        lambda x: f"{x:.4f}s" if x < 1 else f"{x:.2f}s"
    )
    
    # Generate Markdown analysis
    markdown_text = f"""
### Reward-Duration Relationship Analysis

This plot explores the correlation between episode rewards and their durations. Key aspects:

- **Point distribution**: Cluster locations show common reward-duration combinations
- **Regression line**: Black dashed line shows global trend
- **Color coding**: Different modifications' performance patterns

**Statistical Summary:**

{stats_df.to_markdown(index=False)}

**Interpretation Guide:**
- Positive correlation: Higher rewards take longer to achieve
- Negative correlation: Efficient high-reward episodes
- Near-zero: No clear time-reward relationship
"""
    display(Markdown(markdown_text))

    # Create plot from collected data
    plt.figure(figsize=STYLE["figure_size"])
    df = pd.DataFrame(plot_data)
    
    if not df.empty:
        sns.scatterplot(
            data=df,
            x="Reward",
            y="Duration",
            hue="Modification",
            palette=palette,
            edgecolor='w',
            alpha=0.7,
            s=40
        )
        
        # Global regression line
        sns.regplot(
            x=df["Reward"],
            y=df["Duration"],
            scatter=False,
            color='black',
            line_kws={'linestyle': '--'}
        )
    
    # Styling
    plt.title("Reward vs Duration Correlation", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Episode Reward", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("Duration (seconds)", fontsize=STYLE["axis_label_fontsize"])
    plt.grid(**STYLE["grid"])
    plt.legend(
        title="Modifications",
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        frameon=True,
        edgecolor='black'
    )
    plt.tight_layout()
    plt.show()