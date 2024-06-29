def assert_colorswaps(colorswaps):
    msg = "Invalid colorswaps dictionary, needs to be e.g.: {(0, 0, 0): (255, 255, 255), ...}"
    for ecol, rcol in colorswaps.items():
        assert len(ecol) == 3 and len(rcol) == 3, msg
        assert all(0 <= c <= 255 for c in ecol) and all(0 <= c <= 255 for c in rcol), msg


def colorswappinng(image, colorswaps):
    for (r1, g1, b1), (r2, g2, b2) in colorswaps.items():
        red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
        mask1 = (red == r1) & (green == g1) & (blue == b1)
        # mask2 = (red == r2) & (green == g2) & (blue == b2)
        image[:,:,:3][mask1] = [r2, g2, b2]
        # image[:,:,:3][mask2] = [r1, g1, b1]


def inpainting(image, x, y, w, h, subimage):
    # x, y, w, h = y, x, h, w
    x_end = min(x + w, 210)
    y_end = min(y + h, 160)
    image[x:x_end, y:y_end, :] = subimage[:x_end - x, :y_end - y, :]


class ALEColorSwap:
    def __init__(self, ale, colorswaps):
        self._ale = ale
        self._colorswaps = colorswaps

    def __getattr__(self, name):
        if name == "getScreenRGB" or name == "getScreen":
            return self.custom_getScreenRGB
        return getattr(self._ale, name)

    def custom_getScreenRGB(self, *args, **kwargs):
        ret = self._ale.getScreenRGB(*args, **kwargs)
        colorswappinng(ret, self._colorswaps)
        return ret


class ALEInpainting:
    def __init__(self, ale, inpaintings):
        self._ale = ale
        self._inpaintings = inpaintings

    def __getattr__(self, name):
        if name == "getScreenRGB" or name == "getScreen":
            return self.custom_getScreenRGB
        return getattr(self._ale, name)

    def custom_getScreenRGB(self, *args, **kwargs):
        ret = self._ale.getScreenRGB(*args, **kwargs)
        for x, y, w, h, subimage in self._inpaintings:
            inpainting(ret, x, y, w, h, subimage)
        return ret
