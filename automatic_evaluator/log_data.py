from dataclasses import dataclass
from typing import List


@dataclass
class LogData:
    """Container for processed log data"""
    modifications: List[str]
    model_path: str
    game: str
    rewards: List[List[float]]  # Individual step rewards per episode
    actions: List[List[int]]    # Actions taken per episode
    times: List[List[float]]    # Timestamps per episode
    run_label: str             # Pre-formatted label for plots
    epoch_rewards: List[float]
    epoch_times: List[int]
