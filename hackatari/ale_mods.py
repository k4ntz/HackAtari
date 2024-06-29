import numpy as np


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


def inpainting(image, x, y, w, h, subimage):
    # x, y, w, h = y, x, h, w
    x_end = min(x + w, 210)
    y_end = min(y + h, 160)
    image[x:x_end, y:y_end, :] = subimage[:x_end - x, :y_end - y, :]

def masked_inpainting(image, x, y, w, h, subimage, inpaint_colors):
    x_end = min(x + w, 210)
    y_end = min(y + h, 160)
    mask = np.zeros_like(image, dtype=bool)
    for inpaint_color in inpaint_colors:
        mask = np.all(image[x:x_end, y:y_end, :] != inpaint_color, axis=-1)
    image[x:x_end, y:y_end, :] = np.where(mask[..., None], subimage[:x_end - x, :y_end - y, :], image[x:x_end, y:y_end, :])
        
    

class ALEInpainting:
    def __init__(self, ale, inpaintings):
        self._ale = ale
        self._inpaintings = inpaintings
        self._place_above = [(214, 92, 92)]

    def __getattr__(self, name):
        if name == "getScreenRGB" or name == "getScreen":
            return self.custom_getScreenRGB
        return getattr(self._ale, name)

    def custom_getScreenRGB(self, *args, **kwargs):
        ret = self._ale.getScreenRGB(*args, **kwargs)
        for x, y, w, h, subimage in self._inpaintings:
            masked_inpainting(ret, x, y, w, h, subimage, self._place_above)
        return ret
