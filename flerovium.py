

from src.html import Tag
from src.image_text import ImageText


class Flerovium:
    def __init__(self, driver):
        self.driver = driver

    def find_by_label(self, text_search: str):
        im = ImageText(self.driver)
        return im.find_by_tag(Tag.A, text_search)
