from hackatari import HumanPlayable
import cv2
import pygame
import os
import datetime
import json
import argparse


def save_video(frames, folder, game_name, user_id, fps=30):
    """Saves the recorded gameplay as a video file."""
    if not frames:
        print("No frames to save.")
        return

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        folder, f"{game_name}_{user_id}_gameplay_{timestamp}.avi")

    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    for frame in frames:
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    out.release()
    print(f"Video saved as {filename}")


def save_results(score, folder, game_name, user_id, config):
    """Saves the game results and configuration settings in a JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    result_data = {
        "user_id": user_id,
        "game": game_name,
        "timestamp": timestamp,
        "score": score,
        "config": config
    }

    filename = os.path.join(
        folder, f"{game_name}_{user_id}_result_{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(result_data, f, indent=4)

    print(f"Result saved as {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="HackAtari Human Play Recorder")

    # Game and user parameters
    parser.add_argument("-g", "--game", type=str,
                        default="Seaquest", help="Game to be run")
    parser.add_argument("-uid", "--user_id", type=str,
                        required=True, help="User identifier")

    # Environment settings
    parser.add_argument("-obs", "--obs_mode", type=str,
                        default="obj", help="Observation mode (ori, dqn, obj)")
    parser.add_argument("-f", "--frameskip", type=int, default=1,
                        help="Frames skipped after each action + 1 (default = 4)")
    parser.add_argument("-m", "--modifs", nargs="+",
                        default=[], help="List of game modifications")

    # Display and recording options
    parser.add_argument("-v", "--video", action='store_true',
                        help="Save gameplay video")

    args = parser.parse_args()
    config = vars(args)

    # Generate timestamped folder for storing results and recordings
    save_folder = os.path.join("recordings", args.game)
    os.makedirs(save_folder, exist_ok=True)

    # Initialize game environment
    env = HumanPlayable(
        args.game,
        args.modifs,
        [],
        0,
        "",
        game_mode=0,
        difficulty=0,
        render_mode="human",
        obs_mode=args.obs_mode,
        mode="ram",
        hud=False,
        render_oc_overlay=True,
        frameskip=args.frameskip
    )

    # Initialize pygame and recording variables
    pygame.init()
    aggreward = 0
    running = True
    saved_frames = []

    while running:
        env._handle_user_input()
        if not env.paused:
            action = env._get_action()
            obs, reward, terminated, truncated, _ = env.step(action)
            aggreward += reward

            # Save frames if video recording is enabled
            if args.video:
                saved_frames.append(env._state_buffer_rgb[0])

            env.render()

            if terminated or truncated:
                running = False

    pygame.quit()
    print(f"Final Score: {aggreward}")

    # Save results and video
    save_results(aggreward, save_folder, args.game, args.user_id, config)
    if args.video:
        save_video(saved_frames, save_folder, args.game, args.user_id)


if __name__ == "__main__":
    main()
