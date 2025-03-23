from collections import defaultdict
from matplotlib.patches import Patch
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

def plot_reward_modif_distribution(all_logs: List[LogData], selected_game: str):
    """Plot reward distribution with identical parameters"""
    if all_logs == []:
        return

    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    
    # Create DataFrame from logs
    df = pd.DataFrame([
        {"Modification": log.run_label, "Reward": reward} 
        for log in all_logs 
        for reward in log.epoch_rewards
    ])
    
    # Calculate summary statistics for each modification
    stats = df.groupby('Modification')['Reward'].agg(
        ['mean', 'median', 'std', 'min', 'max', 'count']
    ).reset_index()
    stats = stats.round(2)
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
### Term Definitions:
- **Modification**: A specific alteration to the game environment that affects the agent's gameplay.
- **Run**: A single training run with a specific model and game modification.
- **Episode**: A single playthrough of the game, starting from the initial state. One run consists of multiple episodes.
- **Step**: A single action taken by the agent in the game environment during an episode.
- **Reward**: The score obtained by the agent after completing a step or episode.


### Reward Distribution Analysis for {selected_game}

This plot compares the reward distributions across different modifications of the game **{selected_game}**. Each boxplot represents the spread of episode rewards (summed reward of all steps within a single episode) for a specific modification, showcasing the median (central line), interquartile range (box), and potential outliers (dots).

**Key Statistics:**

{stats.to_markdown(index=False)}
"""
    display(Markdown(markdown_text))
    
    # Create the plot
    plt.figure(figsize=STYLE["tall_figure_size"])
    sns.boxplot(
        data=df,
        y="Modification",
        x="Reward",
        order=unique_mods,
        hue_order=unique_mods,
        palette=palette,
        width=0.6,
        linewidth=1.5,
        hue="Modification",
        flierprops=STYLE["flierprops"]
    )
    
    # Styling
    plt.title(f"Distribution of Aggregated Rewards per Episode", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Aggregated Episode Reward", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("")
    plt.grid(**STYLE["grid"])
    plt.axvline(0, **STYLE["zero_line"])
    
    plt.tight_layout()
    plt.show()
    

def plot_acummulated_reward(all_logs: List[LogData], sigma: float=20.0) -> None:
    """Plot cumulative rewards from episode start with clear differentiation"""
    if all_logs == []:
        return
    
    markdown_text = f"""
### Cumulative Reward Progression Within Episodes

This plot shows how rewards accumulate *from the start of each episode* for different configurations. Unlike the previous step-level analysis that aggregated across episodes, this visualization:

- Reveals how reward potential builds up during single episodes
- Highlights early-stage decisions that impact final outcomes

_Smoothing (σ={sigma}) helps identify general trends in cumulative gains._
"""
    display(Markdown(markdown_text))

    fig, ax = plt.subplots(figsize=STYLE["figure_size"])
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    ax.set_title("Cumulative Reward Development Within Episodes", 
                fontsize=STYLE["title_fontsize"])
    
    # Data processing
    for mod in unique_mods:
        log = next(log for log in all_logs if log.run_label == mod)
        step_counts = [len(ep) for ep in log.rewards]
        max_steps = max(step_counts) if step_counts else 0
        
        accumulated = []
        current_sum = 0
        for step_idx in range(max_steps):
            step_rewards = [ep[step_idx] for ep in log.rewards if len(ep) > step_idx]
            current_sum += sum(step_rewards)
            accumulated.append(current_sum)
        
        smoothed = gaussian_filter1d(accumulated, sigma=sigma)
        ax.plot(
            np.arange(1, max_steps + 1),
            smoothed,
            label=mod.replace("\n", " - "),
            color=color_map[mod],
            linewidth=2
        )

    # Standardized styling
    ax.set_xlabel("Step in Episode", fontsize=STYLE["axis_label_fontsize"])
    ax.set_ylabel("Cumulative Episode Reward", 
                 fontsize=STYLE["axis_label_fontsize"])
    ax.legend(
        title=STYLE["legend"]["title"],
        bbox_to_anchor=STYLE["legend"]["bbox_to_anchor"],
        loc=STYLE["legend"]["loc"],
        fontsize=STYLE["legend"]["legend_fontsize"],
        frameon=STYLE["legend"]["frameon"],
    )
    ax.grid(True, **STYLE["grid"])
    ax.axhline(0, **STYLE["zero_line"])
    
    plt.tight_layout()
    plt.subplots_adjust(right=STYLE["subplots_adjust_right"])
    plt.show()



def plot_non_filtered_smoothed_accumulated_rewards(all_logs: List[LogData], sigma: float=20.0) -> None:
    """Plot step-level accumulated rewards with contextual explanation"""
    if all_logs == []:
        return

    markdown_text = f"""
### Step-Level Accumulated Reward Analysis

This visualization drills down into individual steps, showing the smoothed sum of rewards aggregated (summed) *at each step* across all episodes. This reveals:

- **Critical decision points**: Steps with consistently high/low rewards, identifying the trends
- **Action impact**: How individual agent decisions affect long-term outcomes

It is worth mentioning that some game modifications have lower step counts due to shorter episodes. This can lead to some lines ending before others.

_Smoothing (σ={sigma}) reduces noise while preserving trend patterns._
"""
    display(Markdown(markdown_text))

    # Visualization setup
    fig, ax = plt.subplots(figsize=STYLE["figure_size"])
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    ax.set_title("Smoothed Aggregated Rewards Per Step", 
                fontsize=STYLE["title_fontsize"])

    # Data processing and plotting
    for mod in unique_mods:
        log = next(log for log in all_logs if log.run_label == mod)
        max_length = max(len(ep) for ep in log.rewards)
        reward_matrix = np.zeros((len(log.rewards), max_length))
        
        # Create step matrix
        for i, ep in enumerate(log.rewards):
            reward_matrix[i, :len(ep)] = ep
        
        # Calculate accumulated rewards per step
        accumulated_rewards = np.sum(reward_matrix, axis=0)
        smoothed = gaussian_filter1d(accumulated_rewards, sigma=sigma)
        
        ax.plot(
            np.arange(1, len(smoothed) + 1),
            smoothed,
            label=mod.replace("\n", " - "),
            color=color_map[mod],
            linewidth=2
        )

    # Standardized styling
    ax.set_xlabel("Step", fontsize=STYLE["axis_label_fontsize"])
    ax.set_ylabel("Smoothed Aggregated Reward", 
                 fontsize=STYLE["axis_label_fontsize"])
    ax.legend(
        title=STYLE["legend"]["title"],
        bbox_to_anchor=STYLE["legend"]["bbox_to_anchor"],
        loc=STYLE["legend"]["loc"],
        fontsize=STYLE["legend"]["legend_fontsize"],
        frameon=STYLE["legend"]["frameon"],
    )
    ax.grid(True, **STYLE["grid"])
    ax.axhline(0, **STYLE["zero_line"])
    
    plt.tight_layout()
    plt.subplots_adjust(right=STYLE["subplots_adjust_right"])
    plt.show()


def plot_reward_progression(all_logs: List[LogData], selected_game: str):
    """Plot reward progression with standardized styling and contextual description"""
    if all_logs == []:
        return

    markdown_text = f"""
### Reward Progression Analysis for {selected_game}

Building on the distribution analysis, this plot shows how rewards evolve across episodes for each modification of **{selected_game}**. The lines represent aggregated (summed) rewards across the episode, revealing performance trends over multiple episodes.
"""
    display(Markdown(markdown_text))

    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    plt.figure(figsize=STYLE["figure_size"])
    plot_data = []
    for mod in unique_mods:
        log = next(log for log in all_logs if log.run_label == mod)
        for episode, reward in enumerate(log.epoch_rewards, 1):
            plot_data.append({
                "Episode": episode,
                "Reward": reward,
                "Configuration": mod
            })
    
    df = pd.DataFrame(plot_data)
    ax = sns.lineplot(
        data=df,
        x="Episode",
        y="Reward",
        hue="Configuration",
        hue_order=unique_mods,
        estimator="mean",
        errorbar=None,
        linewidth=2.5,
        palette=color_map
    )
    
    # Standardized styling
    ax.axhline(0, **STYLE["zero_line"])
    plt.title(f"Reward Progression Across Episodes", 
             fontsize=STYLE["title_fontsize"])
    plt.xlabel("Episode", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("Aggregated Reward", fontsize=STYLE["axis_label_fontsize"])
    plt.grid(True, **STYLE["grid"])
    ax.legend(
        title=STYLE["legend"]["title"],
        bbox_to_anchor=STYLE["legend"]["bbox_to_anchor"],
        loc=STYLE["legend"]["loc"],
        fontsize=STYLE["legend"]["legend_fontsize"],
        frameon=STYLE["legend"]["frameon"],
    )
    plt.tight_layout()
    plt.show()

########### Unused Functions (adjusted for completeness) ###########

def plot_non_filtered_accumulated_rewards(all_logs: List[LogData]) -> None:
    if all_logs == []:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    unique_mods = _get_sorted_modifications(all_logs)
    
    ax.set_title("Non-Filtered Accumulated Rewards Across Modifications", fontsize=16)
    for mod in unique_mods:
        log = next(log for log in all_logs if log.run_label == mod)
        max_length = max(len(ep) for ep in log.rewards)
        reward_matrix = np.zeros((len(log.rewards), max_length))
        for i, ep in enumerate(log.rewards):
            reward_matrix[i, :len(ep)] = ep
        
        accumulated_rewards = np.sum(reward_matrix, axis=0)
        ax.plot(
            np.arange(1, len(accumulated_rewards) + 1),
            accumulated_rewards,
            label=mod.replace("\n", " - ")
        )

    ax.set_xlabel("Steps", fontsize=12)
    ax.set_ylabel("Accumulated Reward", fontsize=12)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()
