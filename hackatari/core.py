from ocatari.core import OCAtari
import os
import importlib
import pygame
import numpy as np
import random


GameList = ["Amidar","Atlantis", "Asterix", "BankHeist", "BattleZone",
            "Boxing", "Breakout", "Carnival", "ChopperCommand", 
            "DonkeyKong", "FishingDerby", "Freeway", 
            "Frostbite", "Kangaroo", "MontezumaRevenge",
            "MsPacman", "Pong", "Riverraid", "Seaquest",  "Skiing",
            "SpaceInvaders", "Tennis", "Venture", "YarsRevenge"]


class ALEColorSwapProxy:
    def __init__(self, ale, colorswaps):
        self._ale = ale
        self._colorswaps = colorswaps

    def __getattr__(self, name):
        if name == "getScreenRGB" or name == "getScreen":
            return self.custom_getScreenRGB
        return getattr(self._ale, name)

    def custom_getScreenRGB(self, *args, **kwargs):
        # Your custom logic here
        ret = self._ale.getScreenRGB(*args, **kwargs)
        colorswappinng(ret, self._colorswaps)
        return ret


class HackAtari(OCAtari):
    """
    HackAtari provides variation of Atari Learning Environments. 
    It is built on top of OCAtari, which provides object-centric observations.
    """
    def __init__(self, game: str, modifs=[], rewardfunc_path=None, colorswaps=None, *args, **kwargs):
        """
        Initialize the game environment.
        """
        if "frameskip" in kwargs:
            if kwargs["frameskip"] == -1:
                self._frameskip = ""
            else:
                self._frameskip = kwargs["frameskip"]
        elif "NoFrameskip" or "v5" in game:
            self._frameskip = 1
        elif "Determinisitc" or "v5" in game:
            self._frameskip = 4
        else:
            self._frameskip = "0"  # correspond to random frameskip
        kwargs["frameskip"] = 1
        kwargs["render_oc_overlay"] = True
        super().__init__(game, *args, **kwargs)
        covered = False
        for cgame in GameList:
            if cgame in game:
                covered = True
                game = cgame
                break
        if not covered:
            print(f"Game '{game}' not covered yet by OCAtari")
            print("Available games: ", GameList)
            _modif_funcs = lambda x: ([], [])
        else:
            _modif_funcs = importlib.import_module(f"hackatari.games.{game.lower()}")._modif_funcs
        
        self.org_reward = 0
        if rewardfunc_path:
            print(f"Changed reward function to {rewardfunc_path}")
            module_name = os.path.splitext(os.path.basename(rewardfunc_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, rewardfunc_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.new_reward_func = module.reward_function
            self._oca_step = self.step
            self.step = self._step_with_lm_reward

        self.alter_ram_steps, self.alter_ram_reset = _modif_funcs(modifs)
        self._oc_step = self.step
        self._oc_reset = self.reset
        if colorswaps:
            assert_colorswaps(colorswaps)
            self.colorswaps = colorswaps
            # self.step = self._colorswap_step
            # self.reset = self._colorswap_reset
            self.env.env.ale = ALEColorSwapProxy(self.env.env.ale, colorswaps)
        else:
            self.step = self._alter_step
            self.reset = self._alter_reset
    
    def _step_with_lm_reward(self, action):
        obs, game_reward, truncated, terminated, info = self._oca_step(action)
        try:
            reward = self.new_reward_func(self)
        except Exception as e:
            print("Error in new_reward_func: ", e)
            reward = 0
        
        self.org_reward = self.org_reward+game_reward
        info["org_reward"] = self.org_reward
        return obs, reward, truncated, terminated, info
    
    def _alter_step(self, action):
        """
        Take a step in the game environment after altering the ram.
        """
        frameskip = self._frameskip
        if frameskip == 0 or not frameskip:
            frameskip = random.choice((2, 5))
        total_reward = 0.0
        terminated = truncated = False
        for i in range(frameskip):
            for func in self.alter_ram_steps:
                func(self)
            obs, reward, terminated, truncated, info = self._oc_step(action)
            done = terminated or truncated
            total_reward += float(reward)
            if done:
                break
            for func in self.alter_ram_steps:
                func(self)
        # Note that the observation on the done=True frame
        # doesn't matter
        return obs, total_reward, terminated, truncated, info

    def _alter_reset(self, *args, **kwargs):
        ret = self._oc_reset(*args, **kwargs)
        self.org_reward = 0
        for func in self.alter_ram_reset:
            func(self)
        return ret

    def _colorswap_step(self, *args, **kwargs):
        """
        Alter the color according to the colorswaps dictionary while also altering the steps.
        """
        ret = self._alter_step(*args, **kwargs)
        colorswappinng(ret[0], self.colorswaps)
        return ret

    def _colorswap_reset(self, *args, **kwargs):
        """
        Alter the color according to the colorswaps dictionary while also altering the steps.
        """
        ret = self._alter_reset(*args, **kwargs)
        colorswappinng(ret[0], self.colorswaps)
        return ret
    
    def _altered_screen_RGB(self, colorswaps):
        ret = self.getScreenRGB()
        colorswappinng(ret, colorswaps)
        return ret


class HumanPlayable(HackAtari):
    """
    HumanPlayable: Enables human play mode for the game.
    """

    def __init__(self, game, modifs=[], colorswaps={}, *args, **kwargs):
        """
        Initializes the HumanPlayable environment with the specified game and modifications.
        """
        kwargs["render_mode"] = "human"
        kwargs["render_oc_overlay"] = True
        super(HumanPlayable, self).__init__(game, modifs, colorswaps, *args, **kwargs)
        self.reset()
        self.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()



    def run(self):
        '''
        run: Runs the ExtendedHuman environment, allowing human interaction with the game.
        '''
        pygame.init()
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                self.step(action)
                self.render()
        pygame.quit()

    def _get_action(self):
        '''
        _get_action: Gets the action corresponding to the current key press.
        '''
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        '''
        _handle_user_input: Handles user input for the BoxingExtendedHuman environment.
        '''
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # Keyboard key pressed
                if event.key == pygame.K_p:  # 'P': Pause/Resume
                    self.paused = not self.paused

                if event.key == pygame.K_r:  # 'R': Reset
                    self.reset()

                elif (event.key,) in self.keys2actions.keys():  # Env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # Keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)

def assert_colorswaps(colorswaps):
    msg = "Invalid colorswaps dictionary, needs to be e.g.: {(0, 0, 0): (255, 255, 255), ...}"
    for ecol, rcol in colorswaps.items():
        assert len(ecol) == 3 and len(rcol) == 3, msg
        assert all(0 <= c <= 255 for c in ecol) and all(0 <= c <= 255 for c in rcol), msg


def colorswappinng(image, colorswaps):
    for (r1, g1, b1), (r2, g2, b2) in colorswaps.items():
        red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
        mask1 = (red == r1) & (green == g1) & (blue == b1)
        mask2 = (red == r2) & (green == g2) & (blue == b2)
        image[:,:,:3][mask1] = [r2, g2, b2]
        image[:,:,:3][mask2] = [r1, g1, b1]