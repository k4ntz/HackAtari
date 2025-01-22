def static_enemy_position(self):
    """
    Makes the enemy and the blocks unable to move up and down.
    """
    self.set_ram(42, 90)
    self.set_ram(26, 37)


def disable_enemy_movement(self):
    """
    Completely disables enemy movement.
    """
    self.set_ram(40, 0)
    self.set_ram(41, 0)


def disable_block_movement(self):
    """
    Completely disables block movement.
    """
    self.set_ram(24, 0)
    self.set_ram(25, 0)


def _modif_funcs(env, modifs):
    modif_mapping = {
        "static": static_enemy_position,
        "disable_enemy_movement": disable_enemy_movement,
        "disable_block_movement": disable_block_movement,
    }

    for mod in modifs:
        if mod in modif_mapping:
            env.step_modifs.append(modif_mapping[mod])
        else:
            print("Invalid or unknown modification")
