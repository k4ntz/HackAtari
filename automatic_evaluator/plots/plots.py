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


def _get_modifications(modifications: list) -> str:
    """
    Get a string representation of the modifications applied to the environment.
    
    :param modifications: List of modifications applied to the environment.
    :return: String representation of the modifications.
    """
    if not modifications:
        return "None"
    return ', '.join(modifications)

############################################################################################################
######################################### Rewards plots ####################################################
############################################################################################################


# def generate_single_run_description(log_data: LogData, game: str) -> str:
#     """Generate Markdown for single run analysis"""
#     rewards = log_data.epoch_rewards
#     stats = {
#         "Average": np.mean(rewards).round(2),
#         "Max": np.max(rewards),
#         "Min": np.min(rewards),
#         "Std Dev": np.std(rewards).round(2),
#         "Episodes": len(rewards)
#     }
    
#     return f"""
# ## {game} - Single Run Analysis
# **Model**: {log_data.model_path}  
# **Modifications**: {', '.join(log_data.modifications) or 'None'}  

# ### Statistics
# {pd.Series(stats).to_markdown()}

# ### Insights
# - 95% of episodes scored between {np.percentile(rewards, 2.5):.1f} and {np.percentile(rewards, 97.5):.1f}
# - Median reward: {np.median(rewards):.1f}
# """

# def filter_accumulated_rewards(all_logs):
#     """
#     Filter out steps where all modifications have zero rewards and cumulative reward is 0.

#     :param all_logs: List of LogData objects
#     :return: Filtered accumulated rewards for each modification
#     """
#     max_length = max(max(len(ep) for ep in log.rewards) for log in all_logs)

#     # Create a matrix to store accumulated rewards for all modifications
#     accumulated_rewards_all_mods = []

#     for log in all_logs:
#         # Create a matrix where each row is an episode, padded with zeros
#         reward_matrix = np.zeros((len(log.rewards), max_length))
#         for i, ep in enumerate(log.rewards):
#             reward_matrix[i, :len(ep)] = ep

#         # Calculate the accumulated reward for each step across all episodes
#         accumulated_rewards = np.sum(reward_matrix, axis=0)
#         accumulated_rewards_all_mods.append(accumulated_rewards)

#     # Combine accumulated rewards from all modifications to find valid steps
#     accumulated_rewards_all_mods = np.array(accumulated_rewards_all_mods)
#     valid_steps = np.any(accumulated_rewards_all_mods != 0, axis=0)  # Keep steps where at least one modification is non-zero

#     # Filter the data
#     filtered_rewards = []
#     for log, accumulated_rewards in zip(all_logs, accumulated_rewards_all_mods):
#         filtered_accumulated_rewards = accumulated_rewards[valid_steps]
#         filtered_rewards.append((log.run_label, valid_steps, filtered_accumulated_rewards))

#     return filtered_rewards


# def plot_filtered_and_smoothed(filtered_rewards, sigma=5.0):
#     """
#     Generate two plots: one filtered and one filtered and smoothed.

#     :param filtered_rewards: Filtered accumulated rewards for each modification
#     :param sigma: Standard deviation for Gaussian smoothing
#     """
#     fig, axes = plt.subplots(1, 2, figsize=(15, 6))

#     # Plot 1: Filtered Accumulated Rewards
#     ax1 = axes[0]
#     ax1.set_title("Filtered Accumulated Rewards", fontsize=16)
#     for run_label, valid_steps, filtered_accumulated_rewards in filtered_rewards:
#         ax1.plot(
#             range(1, len(filtered_accumulated_rewards) + 1),
#             filtered_accumulated_rewards,
#             label=run_label
#         )
#     ax1.set_xlabel("Filtered Steps", fontsize=12)
#     ax1.set_ylabel("Accumulated Reward", fontsize=12)
#     ax1.legend(fontsize=10, loc='upper left')
#     ax1.grid(True, alpha=0.3, linestyle='--')

#     # Plot 2: Filtered and Smoothed Accumulated Rewards
#     ax2 = axes[1]
#     ax2.set_title("Filtered & Smoothed Accumulated Rewards", fontsize=16)
#     for run_label, valid_steps, filtered_accumulated_rewards in filtered_rewards:
#         smoothed_accumulated_rewards = gaussian_filter1d(filtered_accumulated_rewards, sigma=sigma)
#         ax2.plot(
#             range(1, len(smoothed_accumulated_rewards) + 1),
#             smoothed_accumulated_rewards,
#             label=run_label
#         )
#     ax2.set_xlabel("Filtered Steps", fontsize=12)
#     ax2.set_ylabel("Smoothed Accumulated Reward", fontsize=12)
#     ax2.legend(fontsize=10, loc='upper left')
#     ax2.grid(True, alpha=0.3, linestyle='--')

#     plt.tight_layout()
#     plt.show()











# def generate_heatmap_description(action_counts, selected_game, model_path, modifications) -> str:
#     """
#     Generate a dynamic Markdown description for the heatmap.
    
#     :param action_counts: Dictionary of action frequencies.
#     :param selected_game: Name of the game being evaluated.
#     :param model_path: Path to the trained model being evaluated.
#     :param modifications: List of modifications applied to the environment.
#     :return: Markdown formatted text describing the heatmap and insights.
#     """
#     total_actions = sum(action_counts.values())
#     most_frequent_action = max(action_counts, key=action_counts.get)
#     least_frequent_action = min(action_counts, key=action_counts.get)
    
#     description = f"""## Action Frequency Heatmap

# This heatmap represents the frequency of actions taken by the agent across all evaluation episodes.

# ### Key Insights:
# - **Total Actions:** {total_actions} actions taken across all episodes
# - **Most Frequent Action:** Action ID `{most_frequent_action}` with `{action_counts[most_frequent_action]}` occurrences
# - **Least Frequent Action:** Action ID `{least_frequent_action}` with `{action_counts[least_frequent_action]}` occurrences

# ### Game Information:
# - **Game:** {selected_game}
# - **Modifications:** {', '.join(modifications) if modifications else "None"}
# - **Model Path:** `{model_path}`
# """
    
#     return description




