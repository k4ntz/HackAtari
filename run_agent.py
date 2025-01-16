from ocatari.utils import load_agent
from ocatari import OCAtari
from hackatari import HackAtari
import sys
import torch
# sys.path.insert(0, '../') # noqa
import gymnasium as gym
import pygame
import argparse

parser = argparse.ArgumentParser(description="HackAtari run.py Argument Setter")

parser.add_argument(
    "-g", "--game", type=str, default="Seaquest", help="Game to be run"
)

parser.add_argument(
    "-a",
    "--agent",
    type=str,
    default="",
    help="Path to the cleanrl trained agent to be loaded.",
)
# Argument to enable gravity for the player.
parser.add_argument(
    "-mod",
    "--modifs",
    nargs="+",
    default=[],
    help="List of the modifications to be brought to the game",
)

parser.add_argument(
    "-hu", "--human", action="store_true", help="Let user play the game."
)

parser.add_argument(
    "-m",
    "--movie",
    type=bool,
    default=False,
    help="Movie or Render",
)

parser.add_argument(
    "-sm",
    "--switch_modifs",
    nargs="+",
    default=[],
    help="List of the modifications to be brought to the game after a certain frame",
)

parser.add_argument(
    "-sf",
    "--switch_frame",
    type=int,
    default=0,
    help="Swicht_modfis are applied to the game after this frame-threshold",
)

parser.add_argument(
    "-p",
    "--picture",
    type=int,
    default=0,
    help="Takes a picture after the number of steps provided.",
)

parser.add_argument(
    "-cs",
    "--color_swaps",
    default="",
    help="Colorswaps to be applied to the images.",
)

parser.add_argument(
    "-rf",
    "--reward_function",
    type=str,
    default="",
    help="Replace the default reward fuction with new one in path rf",
)
parser.add_argument(
    "-mo",
    "--game_mode",
    type=int,
    default=0,
    help="Use an alternative ALE game mode",
)
parser.add_argument(
    "-d",
    "--difficulty",
    type=int,
    default=0,
    help="Use an alternative ALE difficulty for the game.",
)

args = parser.parse_args()

env = HackAtari(
    args.game,
    args.modifs,
    args.switch_modifs,
    args.switch_frame,
    args.reward_function,
    args.game_mode,
    args.difficulty,
    render_mode="rgb_array" if args.movie else "human",
    obs_mode="obj",
    mode="ram",
    hud=False,
    render_oc_overlay=True,
    buffer_window_size = 2,
    frameskip=4,
)

if args.movie:
    env = gym.wrappers.RecordVideo(env, f"media/videos")

pygame.init()
if args.agent:
    #agent = load_agent("../OC_Atari/models/Skiing/obj_based_ppo.cleanrl_model", env.action_space.n, env)
    agent = load_agent(args.agent, env.action_space.n, env, "cpu")
    print(f"Loaded agents from {args.agent}")

obs, _ = env.reset()
obs, _ , _ , _ , _ = env.step(0)
done = False

while not done:
    # Human intervention to end the run
    events = pygame.event.get()
    for event in events:
        if (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):  # 'Q': Quit
            done = True
    if args.agent:
        dqn_obs = torch.Tensor(obs).unsqueeze(0)
        action, _, _, _  = agent.get_action_and_value(dqn_obs)
        action = action[0]
    else:
        action = env.action_space.sample()
    # import ipdb; ipdb.set_trace()
    obs, reward, terminated, truncated, _ = env.step(action)
    #print(reward) if reward != 0 else None
    # if reward and args.reward_function:
    #     print(reward)
    if terminated or truncated:
        env.reset()
    # if nstep % 100 == 0:
    #     print(".", end="", flush=True)
    env.render()

if args.movie:        
    env.close_video_recorder()
env.close()
