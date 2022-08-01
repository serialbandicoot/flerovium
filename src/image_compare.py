from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

from enum import Enum, auto, unique


@unique
class MatchType(Enum):

    PERFECT = auto()
    GOOD = auto()
    OK = auto()
    BAD = auto()


class ImageCompare:
    def __init__(self, img1: str, img2: str):
        self.img1 = img1
        self.img2 = img2

    def match(self) -> MatchType:
        img_diff = Image.new("RGBA", Image.open(self.img1).size)

        try:
            mismatch = pixelmatch(
                Image.open(self.img1), Image.open(self.img2), img_diff, includeAA=True
            )
        except ValueError:
            return MatchType.BAD

        accurancy = (mismatch / self.get_num_pixels()) * 100
        if accurancy < 1:
            return MatchType.PERFECT
        elif accurancy < 20:
            return MatchType.GOOD
        elif accurancy < 50:
            return MatchType.OK
        else:
            return MatchType.BAD

    def get_num_pixels(self):
        width, height = Image.open(self.img1).size
        return width * height
