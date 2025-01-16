from hackatari.ale_mods import (
    ALEColorSwap,
    ALEInpainting,
    assert_colorswaps,
)
import random
import numpy as np
import pygame
import importlib
import sys
from ocatari.core import OCAtari
import warnings
import cv2

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


GameList = [
    "Amidar",
    "Atlantis",
    "Asterix",
    "BankHeist",
    "BattleZone",
    "Boxing",
    "Breakout",
    "Carnival",
    "ChopperCommand",
    "DonkeyKong",
    "DoubleDunk",
    "FishingDerby",
    "Freeway",
    "Frostbite",
    "Kangaroo",
    "KungFuMaster",
    "MontezumaRevenge",
    "MsPacman",
    "NameThisGame",
    "Pong",
    "Riverraid",
    "Seaquest",
    "Skiing",
    "SpaceInvaders",
    "Tennis",
    "Venture",
    "YarsRevenge",
]


class HackAtari(OCAtari):
    """
    HackAtari provides variation of Atari Learning Environments.
    It is built on top of OCAtari, which provides object-centric observations.
    """

    def __init__(
        self,
        env_name: str,
        modifs=[],
        switch_modfis=[],
        switch_frame=1000,
        rewardfunc_path=None,
        colorswaps=None,
        dopamine_pooling=True,
        game_mode=0,
        difficulty=0,
        *args,
        **kwargs,
    ):
        """
        Initialize the game environment.
        """
        if kwargs.get("frameskip", False):
            self._frameskip = kwargs["frameskip"]
        else:
            self._frameskip = 4
        kwargs["frameskip"] = 1

        super().__init__(env_name, *args, **kwargs)
        covered = False
        for cgame in GameList:
            if cgame in env_name:
                covered = True
                game = cgame
                break
        if not covered:
            print(f"Game '{env_name}' not covered yet by OCAtari")
            print("Available games: ", GameList)
            # _modif_funcs = lambda x, y: ([], [])
            self._modif_funcs = lambda x, y: ([], [])
        else:
            self._modif_funcs = importlib.import_module(
                f"hackatari.games.{game.lower()}"
            )._modif_funcs

        self.step_modifs, self.reset_modifs, self.post_detection_modifs = [], [], []
        self.inpaintings, self.place_above = [], []
        self._modif_funcs(self, modifs)
        if dopamine_pooling and self._frameskip > 1:
            self.dopamine_pooling = dopamine_pooling
        else:
            self.dopamine_pooling = False
        if self.inpaintings:
            self.env.env.ale = ALEInpainting(
                self.env.env.ale, self.inpaintings, self.place_above
            )
        self._oc_step = self.step
        self._oc_reset = self.reset
        if colorswaps:
            assert_colorswaps(colorswaps)
            self.colorswaps = colorswaps
            self.env.env.ale = ALEColorSwap(self.env.env.ale, colorswaps)
        if switch_modfis:
            self.switch_modfis = switch_modfis
            self.switch_frame = switch_frame
            self.modfis = modifs
            self.step = self._alter_step_with_switch
            self.reset = self._alter_reset_with_switch
        else:
            self.step = self._alter_step
            self.reset = self._alter_reset

        self.org_return = 0
        self.org_reward = 0
        if rewardfunc_path:
            print(f"Changed reward function to {rewardfunc_path}")
            spec = importlib.util.spec_from_file_location(
                "reward_function", rewardfunc_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules["reward_function"] = module
            spec.loader.exec_module(module)
            self.new_reward_func = module.reward_function
            self._hack_step = self.step
            self.step = self._step_with_lm_reward

        try:
            self.env.env.ale.setMode(game_mode)
        except RuntimeError:
            print(
                f"Oops!  That was no valid number. The available modes are {self.env.env.ale.getAvailableModes()}"
            )
            exit()
        try:
            self.env.env.ale.setDifficulty(difficulty)
        except RuntimeError:
            print(
                f"Oops!  That was no valid number. The available difficulties are {self.env.env.ale.getAvailableDifficulties()}"
            )
            exit()

    def _step_with_lm_reward(self, action):
        obs, game_reward, truncated, terminated, info = self._hack_step(action)
        self.org_reward = game_reward
        self.org_return = self.org_return + game_reward
        try:
            reward = self.new_reward_func(self)
        except Exception as e:
            print("Error in new_reward_func: ", e)
            reward = 0

        info["org_return"] = self.org_return
        return obs, reward, truncated, terminated, info

    def _alter_step(self, *args, **kwargs):
        """
        Take a step in the game environment after altering the ram.
        """
        frameskip = self._frameskip
        total_reward = 0.0
        terminated = truncated = False
        if self.dopamine_pooling:
            last_two_obs = []
            last_two_org = []

        for i in range(frameskip-1):
            for func in self.step_modifs:
                func(self)
            obs, reward, terminated, truncated, info = self._env.step(
                *args, **kwargs)
            total_reward += float(reward)
            if terminated or truncated:
                break

        if self.dopamine_pooling:
            last_two_obs.append(cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA))
            last_two_org.append(self.getScreenRGB())

        for func in self.step_modifs:
            func(self)
        obs, reward, terminated, truncated, info = super().step(
            *args, **kwargs)
        total_reward += float(reward)
        for func in self.post_detection_modifs:
            func(self)
        if self.dopamine_pooling:
            last_two_obs.append(cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA))
            last_two_org.append(self.getScreenRGB())

        if self.dopamine_pooling:
            merged_obs = np.maximum.reduce(last_two_obs)
            merged_org = np.maximum.reduce(last_two_org)
            self._state_buffer_dqn[-1] = merged_obs
            self._state_buffer_rgb[-1] = merged_org
            obs[-1] = merged_obs

        return obs, total_reward, terminated, truncated, info

    def _alter_reset(self, *args, **kwargs):
        obs, info = super().reset(*args, **kwargs)
        self.org_reward = 0
        self.org_return = 0
        for func in self.reset_modifs:
            func(self)
        for func in self.post_detection_modifs:
            func(self)
        return obs, info

    def _alter_step_with_switch(self, *args, **kwargs):
        """
        Take a step in the game environment after altering the ram.
        """
        # print(self.step_modifs)
        frameskip = self._frameskip
        if frameskip == 0 or not frameskip:
            frameskip = random.choice((2, 5))
        total_reward = 0.0
        terminated = truncated = False
        for func in self.step_modifs:
            func(self)
        for i in range(frameskip):
            obs, reward, terminated, truncated, info = self._env.step(
                *args, **kwargs)
            total_reward += float(reward)
            for func in self.step_modifs:
                func(self)
            if terminated or truncated:
                break
        # self.detect_objects()
        if (
            self.switch_frame - frameskip
            <= info["episode_frame_number"]
            < self.switch_frame
        ):
            self._modif_funcs(self, self.switch_modfis)
        for func in self.post_detection_modifs:
            func(self)
        # Note that the observation on the done=True frame
        # doesn't matter
        # obs = self._post_step(obs)
        return obs, total_reward, terminated, truncated, info

    def _alter_reset_with_switch(self, *args, **kwargs):
        self.step_modifs, self.reset_modfis = [], []
        self._modif_funcs(self, self.modfis)
        obs, info = super().reset(*args, **kwargs)
        self.org_reward = 0
        self.org_return = 0
        for func in self.reset_modifs:
            func(self)
        for func in self.post_detection_modifs:
            func(self)
        return obs, info

    def render(self, image=None):
        if self.dopamine_pooling:
            return super().render(self._state_buffer_rgb[-1])
        else:
            return super().render()

    # def _colorswap_step(self, *args, **kwargs):
    #     """
    #     Alter the color according to the colorswaps dictionary while also altering the steps.
    #     """
    #     ret = self._alter_step(*args, **kwargs)
    #     colorswappinng(ret[0], self.colorswaps)
    #     return ret

    # def _colorswap_reset(self, *args, **kwargs):
    #     """
    #     Alter the color according to the colorswaps dictionary while also altering the steps.
    #     """
    #     ret = self._alter_reset(*args, **kwargs)
    #     colorswappinng(ret[0], self.colorswaps)
    #     return ret

    # def _altered_screen_RGB(self, colorswaps):
    #     ret = self.getScreenRGB()
    #     colorswappinng(ret, colorswaps)
    #     return ret


class HumanPlayable(HackAtari):
    """
    HumanPlayable: Enables human play mode for the game.
    """

    def __init__(
        self,
        game,
        modifs=[],
        switch_modfis=[],
        switch_frame=1000,
        rewardfunc_path="",
        colorswaps={},
        game_mode=0,
        difficulty=0,
        *args,
        **kwargs,
    ):
        """
        Initializes the HumanPlayable environment with the specified game and modifications.
        """
        kwargs["render_mode"] = "human"
        kwargs["render_oc_overlay"] = True
        kwargs["full_action_space"] = True
        super(HumanPlayable, self).__init__(
            game,
            modifs,
            switch_modfis,
            switch_frame,
            rewardfunc_path,
            colorswaps,
            game_mode,
            difficulty,
            * args,
            **kwargs,
        )
        self.reset()
        self.render()  # Initialize the pygame video system
        self.print_reward = bool(rewardfunc_path)
        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def run(self):
        """
        run: Runs the ExtendedHuman environment, allowing human interaction with the game.
        """
        pygame.init()
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                _, reward, _, _, _ = self.step(action)
                if self.print_reward and reward:
                    print(reward)
                self.render()
        pygame.quit()

    def _get_action(self):
        """
        _get_action: Gets the action corresponding to the current key press.
        """
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        """
        _handle_user_input: Handles user input for the BoxingExtendedHuman environment.
        """
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # Keyboard key pressed
                if event.key == pygame.K_p:  # 'P': Pause/Resume
                    self.paused = not self.paused

                if event.key == pygame.K_q:  # 'Q': Quit
                    self.running = False

                if event.key == pygame.K_r:  # 'R': Reset
                    self.reset()

                elif (event.key,) in self.keys2actions.keys():  # Env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # Keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)
