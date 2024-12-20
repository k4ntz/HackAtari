from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym

from ocatari.utils import load_agent


def save_upsampled(rgb_arrays, k=4, l=4):
    augs = []
    for rgb_array in rgb_arrays:
        aug = np.repeat(np.repeat(rgb_array, k, axis=0),
                        l, axis=1)[:, :, [2, 1, 0]]
        augs.append(aug)
    aug = np.average(augs, 0).astype(int)
    # plt.imshow(aug)
    # plt.show()
    cv2.imwrite("screenshot.png", aug, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print("Screenshot saved as screenshot.png")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="HackAtari run.py Argument Setter")

    parser.add_argument(
        "-g", "--game", type=str, default="Seaquest", help="Game to be run"
    )

    parser.add_argument(
        "-obs",
        "--obs_mode",
        type=str,
        default="obj",
        help="The observation mode (ori, dqn, obj)",
    )

    parser.add_argument(
        "-w",
        "--window",
        type=int,
        default=4,
        help="The buffer window size (default = 4)",
    )

    parser.add_argument(
        "-f",
        "--frameskip",
        type=int,
        default=4,
        help="The frames skipped after each action + 1 (default = 4)",
    )

    parser.add_argument(
        "-dp",
        "--dopamine_pooling",
        type=bool,
        default=False,
        help="Use dopamine like frameskipping (default = False)",
    )

    # Argument to enable gravity for the player.
    parser.add_argument(
        "-m",
        "--modifs",
        nargs="+",
        default=[],
        help="List of the modifications to be brought to the game",
    )

    parser.add_argument(
        "-hu", "--human", action="store_true", help="Let user play the game."
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
        "-a",
        "--agent",
        type=str,
        default="",
        help="Path to the cleanrl trained agent to be loaded.",
    )
    parser.add_argument(
        "-r",
        "--render",
        type=str,
        default="human",
        help="Should the video be displayed (human) or not (rbg_array, None)",
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
    obss = []

    # color_swaps = load_color_swaps(args.color_swaps)

    if args.human:
        env = HumanPlayable(
            args.game,
            args.modifs,
            args.switch_modifs,
            args.switch_frame,
            args.reward_function,
            game_mode=args.game_mode,
            difficulty=args.difficulty,
            render_mode=args.render,
            obs_mode=args.obs_mode,
            mode="ram",
            hud=False,
            render_oc_overlay=True,
            frameskip=1,
        )
        env.run()
    else:
        env = HackAtari(
            args.game,
            args.modifs,
            args.switch_modifs,
            args.switch_frame,
            args.reward_function,
            dopamine_pooling=args.dopamine_pooling,
            game_mode=args.game_mode,
            difficulty=args.difficulty,
            render_mode=args.render,
            obs_mode=args.obs_mode,
            mode="ram",
            hud=False,
            render_oc_overlay=True,
            buffer_window_size=args.window,
            frameskip=args.frameskip,
            repeat_action_probability=0.25,
            full_action_space=False,
        )

        pygame.init()
        if args.agent:
            agent, policy = load_agent(
                args.agent, env, "cpu")
            print(f"Loaded agents from {args.agent}")

        obs, _ = env.reset()
        done = False
        nstep = 1
        tr = 0
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
                action = policy(dqn_obs)[0]
            else:
                action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            tr += reward
            if reward and args.reward_function:
                print(reward)
            if terminated or truncated:
                print(info)
                print(tr)
                tr = 0
                env.reset()
            if nstep == args.picture:
                obss.append(obs)
                save_upsampled(obss)
                exit()
            elif args.picture - nstep < 4:
                obss.append(obs)
            nstep += 1
            env.render()

        env.close()
