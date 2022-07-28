from src.file_helper import FileHelper
from src.html import Tag
from src.image_text import ImageText
from src.db import DB
from src.html import HTML
from src.image_compare import ImageCompare, MatchType
import os
from selenium import webdriver
from src.html import HTML

class Flerovium:
    def __init__(self, driver: webdriver):
        self.driver = driver
        HTML.release_driver_on_loaded(driver)


    def _evaludate_by_selenium(self, label: str):
        # 1. Check JSON Data
        label_data = DB().get_by_label(label)
        if label_data is None:
            return None

        # Links
        if label_data["tag_name"] == "a" and label_data["text"] != None:
            return HTML.find_element_by_link(self.driver, label_data["text"])

        # Input
        if label_data["tag_name"] == "input":
            if label_data["tag_name"] != None:
                return HTML.find_element_by_name(self.driver, label_data["name"])

            if label_data["e_id"] != None:
                return HTML.find_element_by_id(self.driver, label_data["e_id"])

        # Button
        if label_data["tag_name"] == "button":
            if label_data["tag_name"] != None:
                e = HTML.find_element_by_name(self.driver, label_data["name"])
                if e.text == label_data["text"]:
                    return e

            if label_data["id"] != None:
                e = HTML.find_element_by_name(self.driver, label_data["id"])
                if e.text == label_data["text"]:
                    return e

        if label_data["class"] != None:
            e = HTML.find_element_by_class_name(self.driver, label_data["class"])
            if e.text == label_data["text"]:
                return e

        return None

    def _evaluate_by_image(self, label, element: str):
        label_data = DB().get_by_label(label)
        if element and label_data:
            if label_data["tag_name"] != None:
                image_path = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "data",
                    "images",
                    label_data["image_label_name"],
                )
                tmp_path = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "data",
                    "images",
                    str(label_data["id"]),
                )
                if os.path.exists(image_path):
                    tmp_file = FileHelper.create_image_temp(tmp_path, element)
                    ic = ImageCompare(image_path, tmp_file)
                    res = ic.match()
                    FileHelper.remove_image(tmp_path)  # CleanUp
                    if res == MatchType.BAD:
                        return None
                    else:
                        return res
        else:
            return None

    def _high_ranking_function(self, label: str):
        e = self._evaludate_by_selenium(label)
        i = self._evaluate_by_image(label, e)

        if e != None and i != None:
            # High Ranking
            return e
        elif e != None or i != None:
            # Week Ranking
            return e
        else:
            return None

    def find_by_label(self, label: str):
        hrf_element = self._high_ranking_function(label)
        if hrf_element:
            return hrf_element
        else:
            it = ImageText(self.driver)
            tag_a = it.find_by_tag(Tag.A, label)
            if tag_a:
                return tag_a

            tag_input = it.find_by_tag(Tag.INPUT, label)
            if tag_input:
                return tag_input

            tag_button = it.find_by_tag(Tag.BUTTON, label)
            if tag_button:
                return tag_button

            tag_div = it.find_by_tag(Tag.DIV, label)
            if tag_div:
                return tag_div

        return None
