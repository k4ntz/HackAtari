from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display
from typing import Counter, List
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

def action_distribution_barchart(all_logs: List[LogData], selected_game: str):
    """
    Generate action preference analysis with strategic insights
    """
    if not all_logs:  # Handle empty input
        return

    markdown_text = f"""
### Action Analysis for {selected_game}

This visualization reveals the agent's decision-making patterns across different modifications. The bar charts show:

- **Absolute action frequencies**: Total times each action was chosen
- **Strategic biases**: Preferred/dispreferred actions per configuration. Different modifications are assumed to have different distributions of actions
"""
    display(Markdown(markdown_text))

    # Data preparation
    all_actions = sorted({a for log in all_logs for ep in log.actions for a in ep})
    mod_labels = [log.run_label for log in all_logs]
    
    # Calculate global maximum for consistent scaling
    max_count = max(
        max(Counter(a for ep in log.actions for a in ep).values(), default=0)
        for log in all_logs
    ) if all_logs else 1

    # Visualization setup
    n_mods = len(all_logs)
    ncols = 2
    nrows = (n_mods + ncols - 1) // ncols
    
    fig, axes = plt.subplots(nrows, ncols, 
                           figsize=(14, 5*nrows),
                           gridspec_kw={'wspace': 0.3, 'hspace': 0.5})
    
    fig.suptitle(f"Action Selection Count", 
                fontsize=STYLE["title_fontsize"], y=0.95)

    # Use consistent palette
    palette = sns.color_palette(STYLE["palette"], n_colors=len(all_actions))

    # Create subplot for each modification
    for idx, log in enumerate(all_logs):
        ax = axes.flat[idx] if n_mods > 1 else axes
        
        action_counts = Counter(a for ep in log.actions for a in ep)
        counts = [action_counts.get(a, 0) for a in all_actions]
        total_actions = sum(counts)
        
        # Create percentage labels
        percentages = [f'{(c/total_actions)*100:.1f}%' for c in counts]
        
        bars = ax.bar(
            x=range(len(all_actions)),
            height=counts,
            color=palette,
            edgecolor='white',
            linewidth=0.5
        )
        
        # Dual labels: absolute counts + percentages
        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, 
                    height, 
                    f'{height:,}\n({percentage})',
                    ha='center', 
                    va='bottom',
                    fontsize=8)

        ax.set_title(f"{log.run_label}",
                   fontsize=12, pad=12)
        ax.set_xticks(range(len(all_actions)))
        ax.set_xticklabels(all_actions, 
                         rotation=0, 
                         ha='right', 
                         fontsize=9)
        ax.set_ylim(0, max_count * 1.15)  # Breathing room for labels
        ax.yaxis.grid(True, **STYLE["grid"])
        ax.set_ylabel("Action Count", fontsize=STYLE["axis_label_fontsize"])

        # Apply consistent spine styling
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    # Clean empty subplots
    for j in range(len(all_logs), nrows*ncols):
        axes.flat[j].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.9, right=0.92)
    plt.show()

    
def plot_action_transition_heatmaps(all_logs: List[LogData], selected_game: str):
    """
    Plot transition COUNT heatmaps between consecutive actions for each run
    """

    markdown_text = f"""
### Action Transition Patterns

These heatmaps reveal temporal relationships between agent decisions. Key patterns to observe:

- **Common transitions**: Bright squares show frequent action sequences
- **Action loops**: Diagonal patterns indicate repeated same-action choices
- **Modification differences**: Compare how environment changes affect decision chains

Color intensity represents transition frequency (log scale) between consecutive steps.
"""
    display(Markdown(markdown_text))

    all_actions = sorted({a for log in all_logs for ep in log.actions for a in ep})
    action_labels = [str(a) for a in all_actions]
    
    # Create grid layout
    n_mods = len(all_logs)
    ncols = min(2, n_mods)
    nrows = (n_mods + ncols - 1) // ncols
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    fig.suptitle(f"Action Transition Counts", fontsize=16, y=1.02)
    
    # Find global maximum for color scaling
    max_count = 1
    transition_matrices = []
    
    # First pass to calculate all matrices
    for log in all_logs:
        matrix = np.zeros((len(all_actions), len(all_actions)))
        actions = np.concatenate(log.actions)
        
        for i in range(len(actions)-1):
            current_idx = all_actions.index(actions[i])
            next_idx = all_actions.index(actions[i+1])
            matrix[current_idx, next_idx] += 1
        
        transition_matrices.append(matrix)
        max_count = max(max_count, matrix.max())
    
    # Plotting
    for idx, (log, matrix) in enumerate(zip(all_logs, transition_matrices)):
        ax = axes.flat[idx] if n_mods > 1 else axes
        
        sns.heatmap(
            matrix,
            ax=ax,
            cmap='viridis',
            norm=LogNorm(vmin=1, vmax=max_count),
            cbar=False,
            square=True,
            annot=True,
            fmt=".0f",
            annot_kws={'size': 8},
            mask=matrix == 0,
            linewidths=0.5
        )
        
        ax.set_title(log.run_label.replace("\n", " - "), fontsize=10)
        ax.set_xlabel("Next Action", fontsize=9)
        ax.set_ylabel("Current Action", fontsize=9)
        ax.set_xticks(np.arange(len(all_actions)) + 0.5)
        ax.set_yticks(np.arange(len(all_actions)) + 0.5)
        ax.set_xticklabels(action_labels, rotation=0, fontsize=8, ha='center', va='top')
        ax.set_yticklabels(action_labels, rotation=0, fontsize=8, va='center')
        ax.set_xlim(0, len(all_actions))
        ax.set_ylim(len(all_actions), 0)
    
    # Colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=LogNorm(vmin=1, vmax=max_count))
    fig.colorbar(sm, cax=cbar_ax, label='Transition Count (log scale)')
    
    # Hide empty subplots
    for j in range(len(all_logs), nrows*ncols):
        axes.flat[j].axis('off')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.9, hspace=0.4, wspace=0.3)
    plt.show()


def plot_action_transition_heatmaps_corr(all_logs: List[LogData], selected_game: str):
    """
    Plot action transition CORRELATION heatmaps for each run
    """

    markdown_text = f"""
### Action Transition Correlations

This analysis reveals statistical relationships between consecutive actions, complementing the transition frequency heatmaps. The correlation values (Pearson's r) show:

- **Positive values**: Actions that tend to follow each other more than random chance
- **Negative values**: Actions that systematically avoid preceding each other
- **Neutral values**: No significant temporal relationship

_Note: Correlations measure linear relationships, not causal effects._
"""
    display(Markdown(markdown_text))

    # Original visualization code remains unchanged below
    all_actions = sorted({a for log in all_logs for ep in log.actions for a in ep})
    action_labels = [str(a) for a in all_actions]
    
    # Grid layout
    n_mods = len(all_logs)
    ncols = min(2, n_mods)
    nrows = (n_mods + ncols - 1) // ncols
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    fig.suptitle(f"Action Transition Correlations: {selected_game}", fontsize=16, y=1.02)
    
    # Precompute all correlation matrices
    corr_matrices = []
    for log in all_logs:
        actions = np.concatenate(log.actions)
        corr_matrix = np.zeros((len(all_actions), len(all_actions)))
        
        # Vectorized correlation calculation
        current_actions = np.array([all_actions.index(a) for a in actions[:-1]])
        next_actions = np.array([all_actions.index(a) for a in actions[1:]])
        
        # Create one-hot encoded matrices
        current_onehot = np.eye(len(all_actions))[current_actions]
        next_onehot = np.eye(len(all_actions))[next_actions]
        
        # Compute correlations
        corr_matrix = np.corrcoef(current_onehot.T, next_onehot.T)[:len(all_actions), len(all_actions):]
        corr_matrices.append(corr_matrix)
    
    # Plotting
    for idx, (log, corr_matrix) in enumerate(zip(all_logs, corr_matrices)):
        ax = axes.flat[idx] if n_mods > 1 else axes
        
        sns.heatmap(
            corr_matrix,
            ax=ax,
            cmap='coolwarm',
            vmin=-1,
            vmax=1,
            square=True,
            annot=True,
            fmt=".2f",
            annot_kws={'size': 8},
            linewidths=0.5,
            cbar=False
        )
        
        ax.set_title(log.run_label.replace("\n", " - "), fontsize=10)
        ax.set_xlabel("Next Action", fontsize=9)
        ax.set_ylabel("Current Action", fontsize=9)
        ax.set_xticks(np.arange(len(all_actions)) + 0.5)
        ax.set_yticks(np.arange(len(all_actions)) + 0.5)
        ax.set_xticklabels(action_labels, rotation=0, fontsize=8, ha='center', va='top')
        ax.set_yticklabels(action_labels, rotation=0, fontsize=8, va='center')
        ax.set_xlim(0, len(all_actions))
        ax.set_ylim(len(all_actions), 0)
    
    # Add a single shared colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=-1, vmax=1))
    fig.colorbar(sm, cax=cbar_ax, label='Pearson Correlation')
    
    # Hide empty subplots
    if n_mods > 1:
        for j in range(len(all_logs), nrows*ncols):
            axes.flat[j].axis('off')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.9, hspace=0.4, wspace=0.3)
    plt.show()