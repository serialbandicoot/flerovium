from src.file_helper import FileHelper
from src.html import Tag
from src.image_text import ImageText
from src.db import DB
from src.html import HTML
from src.image_compare import ImageCompare, MatchType
import os
from selenium import webdriver
from src.html import HTML
from functools import partial


class MethodMissing:
    def method_missing(self, name, *args, **kwargs):
        """please implement"""
        raise NotImplementedError('please implement a "method_missing" method')

    def __getattr__(self, name):
        return partial(self.method_missing, name)


class Flerovium(MethodMissing):

    element = None

    def __init__(self, driver: webdriver):
        self.driver = driver
        HTML.release_driver_on_loaded(driver)

    def _evaluate_by_selenium(self, label: str):
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
                if label_data["name"] != "":
                    return HTML.find_element_by_name(self.driver, label_data["name"])

                if label_data["class"] != "":
                    return HTML.find_element_by_class_name(
                        self.driver, label_data["class"]
                    )

                if label_data["e_id"] != None:
                    return HTML.find_element_by_id(self.driver, label_data["e_id"])

        # Button
        if label_data["tag_name"] == "button":
            if label_data["name"] != "":
                e = HTML.find_element_by_name(self.driver, label_data["name"])
                if e.text == label_data["text"]:
                    return e

            if label_data["e_id"] != "":
                e = HTML.find_element_by_id(self.driver, label_data["e_id"])
                if e.text == label_data["text"]:
                    return e

            if label_data["class"] != "":
                e = HTML.find_element_by_class_name(self.driver, label_data["class"])
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
        e = self._evaluate_by_selenium(label)
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
            self.element = hrf_element
            return self
        else:
            it = ImageText(self.driver)
            tag_a = it.find_by_tag(Tag.A, label)
            if tag_a:
                self.element = tag_a
                return self

            tag_input = it.find_by_tag(Tag.INPUT, label)
            if tag_input:
                self.element = tag_input
                return self

            tag_button = it.find_by_tag(Tag.BUTTON, label)
            if tag_button:
                self.element = tag_button
                return self

            tag_div = it.find_by_tag(Tag.DIV, label)
            if tag_div:
                self.element = tag_div
                return self

            tag_div = it.find_by_tag(Tag.FORM, label)
            if tag_div:
                self.element = tag_div
                return self

        # No elements found!
        self.driver.save_screenshot("error.png")

        return self

    def method_missing(self, name, *args, **kwargs):
        if name in dir(self.element):
            method = getattr(self.element, name)
            if callable(method):
                return method(*args, **kwargs)
            else:
                raise AttributeError(
                    ' %s has not method named "%s" ' % (self.item, name)
                )

        return None
