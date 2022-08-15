import os
import shutil
import tempfile
from functools import partial
from typing import Union

from selenium import webdriver

from src.client import Client
from src.file_helper import FileHelper
from src.helper import random_string
from src.html_selenium import HTMLSelenium
from src.html_selenium import Tag
from src.image_compare import ImageCompare, MatchType
from src.image_text import ImageText
from src.tag import Tag


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
        HTMLSelenium.release_driver_on_loaded(driver)

    def _evaluate_by_selenium(self, label_data: str):
        if label_data is None:
            return None

        # Links
        if label_data["tag_name"] == "a" and label_data["text"] != None:
            return HTMLSelenium.find_element_by_link(self.driver, label_data["text"])

        # Input
        if label_data["tag_name"] == "input":
            if label_data["tag_name"] != None:
                if label_data["name"] != "":
                    return HTMLSelenium.find_element_by_name(
                        self.driver, label_data["name"]
                    )

                if label_data["class"] != "":
                    return HTMLSelenium.find_element_by_class_name(
                        self.driver, label_data["class"]
                    )

                if label_data["e_id"] != None:
                    return HTMLSelenium.find_element_by_id(
                        self.driver, label_data["e_id"]
                    )

        # Button
        if label_data["tag_name"] == "button":
            if label_data["name"] != "":
                e = HTMLSelenium.find_element_by_name(self.driver, label_data["name"])
                if e.text == label_data["text"]:
                    return e

            if label_data["e_id"] != "":
                e = HTMLSelenium.find_element_by_id(self.driver, label_data["e_id"])
                if e.text == label_data["text"]:
                    return e

            if label_data["class"] != "":
                e = HTMLSelenium.find_element_by_class_name(
                    self.driver, label_data["class"]
                )
                if e.text == label_data["text"]:
                    return e

        if label_data["class"] != None:
            e = HTMLSelenium.find_element_by_class_name(
                self.driver, label_data["class"]
            )
            if e.text == label_data["text"]:
                return e

        return None

    def _get_random_file(self):
        return os.path.join(tempfile.gettempdir(), f"{random_string()}.png")

    def _get_server_image(self, image_name):
        server_img = self._get_random_file()
        response = Client().get_raw_image(image_name)
        with open(server_img, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return server_img

    def _create_local_image_file(self, element):
        local_img = self._get_random_file()
        FileHelper.create_image_from_element(local_img, element)
        return local_img

    def _image_compare(self, server_img, local_img):
        ic = ImageCompare(server_img, local_img)
        res = ic.match()
        FileHelper.remove_image(server_img)  # CleanUp
        FileHelper.remove_image(local_img)  # CleanUp
        if res == MatchType.BAD:
            return None
        else:
            return res

    def _evaluate_by_image(self, label_data, element: str):
        if element and label_data:
            # todo: better check on element data
            if label_data["tag_name"] != None:
                server_img = self._get_server_image(label_data["image_name"])
                local_img = self._create_local_image_file(element)

                return self._image_compare(server_img, local_img)

        else:
            return None

    def _high_ranking_function(self, label: str):
        label_data = Client().get_by_label(label)
        e = self._evaluate_by_selenium(label_data)
        if e is None:
            i = None
        else:
            i = self._evaluate_by_image(label_data, e)

        if e != None and i != None:
            # High Ranking
            return e
        elif e != None or i != None:
            # Week Ranking
            return e
        else:
            return None

    def find_by_label(self, label: str, tag: Union[None, Tag] = None):
        hrf_element = self._high_ranking_function(label)
        if hrf_element:
            self.element = hrf_element
            return self
        elif tag is None:
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
        elif tag is not None:
            it = ImageText(self.driver)
            tag_e = it.find_by_tag(tag, label)
            if tag_e:
                self.element = tag_e
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

    def cnn(self, label: str, site: str, save_path: str):
        file = f"{label}-{site}-{random_string()}"
        full_path = os.path.join(save_path, f"{file}.png")

        it = ImageText(self.driver)
        # limit by tag "A" for now
        tag_a = it.find_by_tag(Tag.A, label, full_path, db_save=False)
        if tag_a:
            return self

    def text(self):
        try:
            text = self.element.text
            if text == "":
                return self.element.get_attribute("value")
            return text
        except Exception as e:
            pass

        return ""
