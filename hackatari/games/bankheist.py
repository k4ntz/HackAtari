TOWNS_VISITED = []

def unlimited_gaz(self):
    """
    Unlimited gaz all the enemies.
    """
    self.set_ram(86, 0)

def no_police(self):
    """
    Unlimited gaz all the enemies.
    """
    ram = self.get_ram()
    for i in range(3):
        if ram[24+i] == 254:
            self.set_ram(24+i, 0)

def only_police(self):
    """
    Unlimited gaz all the enemies.
    """
    ram = self.get_ram()
    for i in range(3):
        if ram[24+i] == 253:
            self.set_ram(24+i, 254)


def revisit_city(self):
    """
    Unlimited gaz all the enemies.
    """
    # TODO: To be implemented


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "unlimited_gaz":
            step_modifs.append(unlimited_gaz)
        elif mod == "no_police":
            step_modifs.append(no_police)
        elif mod == "only_police":
            step_modifs.append(only_police)
    return step_modifs, reset_modifs