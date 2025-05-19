from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
from hackatari.utils import HackAtariArgumentParser
from ocatari.utils import load_agent


def save_upsampled(rgb_arrays, k=4, l=4):
    """Upsamples and saves a screenshot."""
    if not rgb_arrays:
        print("No frames to save.")
        return

    augs = [np.repeat(np.repeat(rgb, k, axis=0), l, axis=1)[
        :, :, [2, 1, 0]] for rgb in rgb_arrays]
    aug = np.average(augs, axis=0).astype(int)
    cv2.imwrite("screenshot.png", aug, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print("Screenshot saved as screenshot.png")


def main():
    parser = HackAtariArgumentParser(description="HackAtari Argument Setter")

    parser.add_argument("-g", "--game", type=str,
                        default="Seaquest", help="Game to be run")
    parser.add_argument("-obs", "--obs_mode", type=str,
                        default="obj", help="The observation mode (ori, dqn, obj)")
    parser.add_argument("-w", "--window", type=int, default=4,
                        help="The buffer window size (default = 4)")
    parser.add_argument("-f", "--frameskip", type=int, default=4,
                        help="Frames skipped after each action + 1 (default = 4)")
    parser.add_argument("-dp", "--dopamine_pooling",
                        action='store_true', help="Use dopamine-like frameskipping")
    parser.add_argument("-m", "--modifs", nargs="+", default=[],
                        help="List of modifications to the game")
    parser.add_argument("-hu", "--human", action="store_true",
                        help="Let user play the game.")
    parser.add_argument("-p", "--picture", type=int, default=0,
                        help="Takes a picture after the given steps.")
    parser.add_argument("-rf", "--reward_function", type=str,
                        default="", help="Custom reward function path")
    parser.add_argument("-a", "--agent", type=str,
                        default="", help="Path to trained agent.")
    parser.add_argument("-r", "--render", type=str, default="human",
                        help="Render mode (human, rgb_array, None)")
    parser.add_argument("-mo", "--game_mode", type=int,
                        default=0, help="Alternative ALE game mode")
    parser.add_argument("-d", "--difficulty", type=int,
                        default=0, help="Alternative ALE difficulty")

    args = parser.parse_args()
    obss = []

    if args.human:
        env = HumanPlayable(
            args.game, args.modifs, args.reward_function,
            game_mode=args.game_mode, difficulty=args.difficulty, render_mode=args.render,
            obs_mode=args.obs_mode, mode="ram", hud=False, render_oc_overlay=True, frameskip=1
        )
        env.run()
    else:
        env = HackAtari(
            args.game, args.modifs, args.reward_function,
            dopamine_pooling=args.dopamine_pooling, game_mode=args.game_mode, difficulty=args.difficulty,
            render_mode=args.render, obs_mode=args.obs_mode, mode="ram", hud=False,
            render_oc_overlay=True, buffer_window_size=args.window, frameskip=args.frameskip,
            repeat_action_probability=0.25, full_action_space=False
        )

        pygame.init()
        if args.agent:
            import torch
            _, policy = load_agent(args.agent, env, "cpu")
            print(f"Loaded agent from {args.agent}")

        obs, _ = env.reset()
        done = False
        nstep = 1
        tr = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    done = True

            action = policy(torch.Tensor(obs).unsqueeze(0))[
                0] if args.agent else env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            tr += reward

            if reward and args.reward_function:
                print(reward)

            if terminated or truncated:
                print(info, tr)
                tr = 0
                env.reset()

            if nstep == args.picture:
                obss.append(obs)
                save_upsampled(obss)
                exit()
            elif args.picture - nstep < 4:
                obss.append(obs)

            nstep += 1
            env.render(env._state_buffer_rgb[-1])

        env.close()


if __name__ == "__main__":
    main()
