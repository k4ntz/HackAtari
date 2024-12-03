def no_radar(self):
    """
    Removes the radar content
    """
    self.set_ram(82, 255)
    self.set_ram(83, 255)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "no_radar":
            env.step_modifs.append(no_radar)
