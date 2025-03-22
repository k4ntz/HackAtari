import numpy as np
import json
import gzip
import shutil
from typing import Literal, List, Dict

from log_data import LogData

def log_episode_data(log_file, episode_data):
    """appends new episode data at the end of the log json

    Args:
        log_file (str): path of the log file
        episode_data (dict): episode values
    """
    with open(log_file, 'a') as f:
        json.dump(episode_data, f)
        f.write('\n')

def compress_log_data(log_file, compressed_file):
    """compresses log json file

    Args:
        log_file (str): path of the log file
        compressed_file (str): path of the compressed file
    """
    with open(log_file, 'rb') as f_in, gzip.open(compressed_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def decompress_log_data(compressed_file, decompressed_file):
    """decompresses compressed file into json log file

    Args:
        compressed_file (str): path of the compressed file
        decompressed_file (str): path of the decompressed file
    """
    with gzip.open(compressed_file, 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def read_log_data(log_file):
    """Reads log file into python list

    Args:
        log_file (str): path of the log file

    Returns:
        list: list of dictionaries where each dictionary is an episode_data
    """
    with open(log_file, 'r') as f:
        return [json.loads(line) for line in f]

def combine_means_and_stds(mu_list, sigma_list, n_list):
    """
    Combine multiple means and standard deviations using their respective sample sizes.

    Args:
        mu_list (list): List of means.
        sigma_list (list): List of standard deviations.
        n_list (list): List of sample sizes.

    Returns:
        tuple: Combined mean and combined standard deviation.
    """
    if not (len(mu_list) == len(sigma_list) == len(n_list)):
        raise ValueError("All input lists must have the same length.")

    total_n = sum(n_list)
    combined_mean = sum(n * mu for mu, n in zip(mu_list, n_list)) / total_n
    combined_variance = sum(
        n * (sigma**2 + (mu - combined_mean)**2)
        for mu, sigma, n in zip(mu_list, sigma_list, n_list)
    ) / total_n
    combined_std = np.sqrt(combined_variance)

    return combined_mean, combined_std

def print_metrics(episode_data, args_episodes):
    """prints metrics from a log file's content

    Args:
        episode_data (dict): episode values
        args_episodes (int): number of episodes each evaluation is ran
    """
    unique_agents = list({episode["agent_path"]: None for episode in episode_data}.keys()) # this preserves the agent path order
    episode_data_grouped_by_agent = [[episode for episode in episode_data if episode["agent_path"] == agent] for agent in unique_agents]

    all_episodes_avg_rewards = []
    all_episodes_std_rewards = []
    all_episodes_avg_times = []
    all_episodes_std_times = []
    all_episodes_avg_steps = []
    all_episodes_std_steps = []
    total_runs = []

    for unique_agent, agent_group in zip(unique_agents, episode_data_grouped_by_agent):
        print(f"Loaded agent from {unique_agent}")
        
        all_episodes_cumulative_rewards = []
        all_episodes_cumulative_times = []
        all_episodes_cumulative_actions = []
        all_episodes_cumulative_steps = []

        for episode, episode_data in enumerate(agent_group):
            agent_path = episode_data["agent_path"]
            current_episodes_rewards = episode_data["current_episodes_rewards"]
            current_episodes_times = episode_data["current_episodes_times"]
            current_episodes_actions = episode_data["current_episodes_actions"]

            episodes_cumulative_reward = sum(current_episodes_rewards)            
            all_episodes_cumulative_rewards.append(episodes_cumulative_reward)
            
            episodes_cumulative_time = sum(current_episodes_times)
            all_episodes_cumulative_times.append(episodes_cumulative_time)

            episodes_cumulative_action = {ac:current_episodes_actions.count(ac) for ac in current_episodes_actions}
            episodes_cumulative_action = dict(sorted(episodes_cumulative_action.items()))
            all_episodes_cumulative_actions.append(episodes_cumulative_action)

            episodes_cumulative_step = len(current_episodes_times)
            all_episodes_cumulative_steps.append(episodes_cumulative_step)

            print(f"Episode {episode + 1}: Reward = {episodes_cumulative_reward}, Time = {episodes_cumulative_time:.2f} seconds with {episodes_cumulative_step} steps and actions: {episodes_cumulative_action}")

        all_episodes_avg_reward = np.mean(all_episodes_cumulative_rewards)
        all_episodes_std_reward = np.std(all_episodes_cumulative_rewards)
        all_episodes_avg_rewards.append(all_episodes_avg_reward)
        all_episodes_std_rewards.append(all_episodes_std_reward)

        all_episodes_avg_time = np.mean(all_episodes_cumulative_times)
        all_episodes_std_time = np.std(all_episodes_cumulative_times)
        all_episodes_avg_times.append(all_episodes_avg_time)
        all_episodes_std_times.append(all_episodes_std_time)

        all_episodes_avg_step = np.mean(all_episodes_cumulative_steps)
        all_episodes_std_step = np.std(all_episodes_cumulative_steps)
        all_episodes_avg_steps.append(all_episodes_avg_step)
        all_episodes_std_steps.append(all_episodes_std_step)

        total_runs.append(args_episodes)

        print("\nSummary:")
        print(f"Agent: {agent_path}")
        print(f"Total Episodes: {args_episodes}")

        print(f"Average Reward: {all_episodes_avg_reward:.2f}")
        print(f"Reward Standard Deviation: {all_episodes_std_reward:.2f}")
        print(f"Min Reward: {np.min(all_episodes_cumulative_rewards)}")
        print(f"Max Reward: {np.max(all_episodes_cumulative_rewards)}")

        print(f"Average Time: {all_episodes_avg_time:.2f} seconds")
        print(f"Time Standard Deviation: {all_episodes_std_time:.2f} seconds")
        print(f"Min Time: {np.min(all_episodes_cumulative_times):.2f} seconds")
        print(f"Max Step: {np.max(all_episodes_cumulative_times):.2f} seconds")

        print(f"Average Step: {all_episodes_avg_step:.2f} steps")
        print(f"Step Standard Deviation: {all_episodes_std_step:.2f} steps")
        print(f"Min Step: {np.min(all_episodes_cumulative_steps)} steps")
        print(f"Max Step: {np.max(all_episodes_cumulative_steps)} steps")

        print("--------------------------------------")

    # Compute overall statistics
    total_avg, total_std = combine_means_and_stds(all_episodes_avg_rewards, all_episodes_std_rewards, total_runs)
    total_avg_time, total_std_time = combine_means_and_stds(all_episodes_avg_times, all_episodes_std_times, total_runs)
    total_avg_step, total_std_step = combine_means_and_stds(all_episodes_avg_steps, all_episodes_std_steps, total_runs)
    print("------------------------------------------------")
    print(f"Overall Average Reward: {total_avg:.2f}, Time: {total_avg_time:.2f} seconds and {total_avg_step:.2f} steps")
    print(f"Overall Reward Standard Deviation: {total_std:.2f}, Time Standard Deviation: {total_std_time:.2f} seconds, Step Standard Deviation: {total_std_step:.2f}")
    print("------------------------------------------------")

def get_log_data(episode_data, data_type: Literal["time", "action", "reward"]):
    """returns wanted measurement type from the log

    Args:
        episode_data (list): list of dictionaries where each dictionary is data from a episode
        data_type (Literal['time', 'action', 'reward']): type of data to retrieve from log

    Returns:
        list: list of tuples that contains agent's path and it's measurements
    """
    
    unique_agents = list({episode["agent_path"]: None for episode in episode_data}.keys())
    episode_data_grouped_by_agent = [[episode for episode in episode_data if episode["agent_path"] == agent] for agent in unique_agents]

    # this list will hold every measurement done during the evaluation
    all_episode_data = []

    for unique_agent, agent_group in zip(unique_agents, episode_data_grouped_by_agent):
        # now we will append all data about the unique_agent's trainings
        all_episode_data.append((unique_agent, []))
        for episode, episode_data in enumerate(agent_group):
            current_episodes_data = episode_data[f"current_episodes_{data_type}s"]
            # append every episodes' index and data into the list of the unique_agent's tuple
            all_episode_data[-1][1].append((episode, current_episodes_data))

    return all_episode_data

def format_run_label(model_path: str, modifications: List[str]) -> str:
    """Create consistent run labels"""
    # mod_str = get_modifications(modifications)
    # print(mod_str)
    return f"{model_path}\nMods: {modifications}"


def process_logs(logs: List[Dict], selected_game: str, model_path) -> List[LogData]:
    """Process raw logs into structured LogData objects"""
    processed = []
    
    for log_entry in logs:
        # Extract raw episode data
        episodes = log_entry["log"]
        
        processed.append(LogData(
            modifications=log_entry["modifications"],
            model_path=model_path,
            game=log_entry["game"],
            rewards=[e["current_episodes_rewards"] for e in episodes],
            actions=[e['current_episodes_actions'] for e in episodes],
            times=[e['current_episodes_times'] for e in episodes],
            epoch_rewards=[sum(e["current_episodes_rewards"]) for e in episodes],
            epoch_times=[sum(e["current_episodes_times"]) for e in episodes],
            run_label=str(log_entry["modifications"]),
        ))
    
    return processed

def load_logs(log_infos: List[Dict]):
    logs = []
    for log_info in log_infos:
        log_name = log_info["log_name"]
        decompress_log_data(log_name.replace(".json", "_comp.gz"), log_name)
        log = read_log_data(log_name)    
        logs.append({"log": log, "modifications": log_info["modifications"], "game": log_info["game"], "model": log_info["model"]})

    return logs
