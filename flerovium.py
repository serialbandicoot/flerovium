from src.html import Tag
from src.image_text import ImageText


class Flerovium:
    def __init__(self, driver):
        self.driver = driver

    def find_by_label(self, text_search: str):
        it = ImageText(self.driver)
        tag_a = it.find_by_tag(Tag.A, text_search)
        if tag_a:
            return tag_a
        
        tag_input = it.find_by_tag(Tag.INPUT, text_search)
        if tag_input:
            return tag_input

        tag_button = it.find_by_tag(Tag.BUTTON, text_search)
        if tag_button:
            return tag_button

        return 
