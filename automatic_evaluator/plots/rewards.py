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


def generate_rewards_table(all_logs: List[LogData], selected_game: str) -> None:
    """Generate a simplified single-table analysis with 'None' first, others sorted by Avg descending."""
    stats = []
    for log in all_logs:
        rewards = log.epoch_rewards
        stats.append({
            "Configuration": log.run_label.replace("\n", " - "),
            "Avg": np.mean(rewards),
            "Max": np.max(rewards),
            "Min": np.min(rewards),
            "Std": np.std(rewards),
            "Episodes": len(rewards)
        })
    
    df = pd.DataFrame(stats)
    # Split 'None' and sort others by Avg descending
    none_mask = df['Configuration'] == 'None'
    none_df = df[none_mask]
    others_df = df[~none_mask].sort_values("Avg", ascending=False)
    df = pd.concat([none_df, others_df])
    
    formatted_df = df.copy()
    formatted_df["Avg"] = df["Avg"].map("{:.2f}".format)
    formatted_df["Std"] = df["Std"].map("{:.2f}".format)
    formatted_df["Max"] = df["Max"].map("{:.0f}".format)
    formatted_df["Min"] = df["Min"].map("{:.0f}".format)
    
    result = f"""
        # {selected_game} - Performance Summary

        {formatted_df.to_markdown(index=False)}
    """
    display(Markdown(result))


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
    
    df = pd.DataFrame([
        {"Modification": log.run_label, "Reward": reward} 
        for log in all_logs 
        for reward in log.epoch_rewards
    ])
    
    plt.figure(figsize=STYLE["tall_figure_size"])
    
    # Create boxplot with same parameters
    sns.boxplot(
        data=df,
        y="Modification",
        x="Reward",
        order=unique_mods,  # Reverse order for vertical alignment
        palette=palette,
        width=0.6,
        linewidth=1.5,
        hue="Modification",
        flierprops=STYLE["flierprops"]
    )
    
    # Styling
    plt.title(f"Reward Distribution: {selected_game}", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Episode Reward", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("")
    plt.grid(**STYLE["grid"])
    plt.axvline(0, **STYLE["zero_line"])
    
    plt.tight_layout()
    plt.show()
    

def plot_acummulated_reward(all_logs: List[LogData], sigma: float=20.0) -> None:
    """Plot accumulated rewards with standardized styling"""
    if all_logs == []:
        return

    fig, ax = plt.subplots(figsize=STYLE["figure_size"])
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    ax.set_title("Step-wise Accumulated Rewards Across Episodes", fontsize=STYLE["title_fontsize"])
    
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

    # Apply standardized formatting
    ax.set_xlabel("Step Index in Episode", fontsize=STYLE["axis_label_fontsize"])
    ax.set_ylabel("Smoothed Accumulated Reward", fontsize=STYLE["axis_label_fontsize"])
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
    """Plot non-filtered rewards with standardized styling"""
    if all_logs == []:
        return

    fig, ax = plt.subplots(figsize=STYLE["figure_size"])
    unique_mods = _get_sorted_modifications(all_logs)
    palette = sns.color_palette(STYLE["palette"], n_colors=len(unique_mods))
    color_map = {mod: color for mod, color in zip(unique_mods, palette)}
    
    ax.set_title("Non-Filtered & Smoothed Accumulated Rewards", fontsize=STYLE["title_fontsize"])

    for mod in unique_mods:
        log = next(log for log in all_logs if log.run_label == mod)
        max_length = max(len(ep) for ep in log.rewards)
        reward_matrix = np.zeros((len(log.rewards), max_length))
        for i, ep in enumerate(log.rewards):
            reward_matrix[i, :len(ep)] = ep
        
        accumulated_rewards = np.sum(reward_matrix, axis=0)
        smoothed = gaussian_filter1d(accumulated_rewards, sigma=sigma)
        ax.plot(
            np.arange(1, len(smoothed) + 1),
            smoothed,
            label=mod.replace("\n", " - "),
            color=color_map[mod],
            linewidth=2
        )

    # Apply standardized formatting
    ax.set_xlabel("Steps", fontsize=STYLE["axis_label_fontsize"])
    ax.set_ylabel("Smoothed Accumulated Reward", fontsize=STYLE["axis_label_fontsize"])
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
    """Plot reward progression with standardized styling"""
    if all_logs == []:
        return

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
    
    # Apply standardized formatting
    ax.axhline(0, **STYLE["zero_line"])
    plt.title(f"Reward Progression Across Evaluations\n{selected_game}", fontsize=STYLE["title_fontsize"])
    plt.xlabel("Evaluation Episode", fontsize=STYLE["axis_label_fontsize"])
    plt.ylabel("Episode Reward", fontsize=STYLE["axis_label_fontsize"])
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
