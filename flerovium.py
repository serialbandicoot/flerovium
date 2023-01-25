import os
import shutil
import tempfile
import json
from functools import partial
from typing import Union
from PIL import Image
from selenium import webdriver

from src.client import Client
from src.file_helper import FileHelper
from src.helper import random_string
from src.html_selenium import HTMLSelenium
from src.html_selenium import Tag
from src.image_compare import ImageCompare, MatchType
from src.image_text import ImageText
from src.logging import Logging
from src.tag import Tag
from selenium.common.exceptions import WebDriverException
from keras.preprocessing import image
from keras.models import load_model
from operator import itemgetter
import uuid

class MethodMissing:
    def method_missing(self, name, *args, **kwargs):
        """please implement"""
        raise NotImplementedError('please implement a "method_missing" method')

    def __getattr__(self, name):
        return partial(self.method_missing, name)


class Flerovium(MethodMissing):

    element = None
    label   = None

    def __init__(self, driver: webdriver):
        self.driver = driver
        self._training_mode = False
        self._logging_mode  = False
        self.fl_id = uuid.uuid4().hex
        
        HTMLSelenium.release_driver_on_loaded(driver)

    @property
    def training_mode(self):
        return self._training_mode

    @training_mode.setter
    def training_mode(self, training: bool):
        self._training_mode = training     

    @property
    def logging_mode(self):
        return self._logging_mode

    @logging_mode.setter
    def logging_mode(self, logging: bool):
        self._logging_mode = logging  

    def _evaluate_by_selenium(self, label_data: dict):
        if label_data is None:
            return None

        tagName = label_data["tag_name"].lower()
        
        # Links
        if tagName == "a" and label_data["text"] != None and label_data["text"] != '':
            return HTMLSelenium.find_element_by_link(self.driver, label_data["text"])

        # Input
        if tagName == "input":
            if tagName != None:
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
        if tagName == "button":
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
            if e is None:
                return None

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

    def _evaluate_by_cnn(self, label: str):
        classes = ['Login', 'SignIn', 'SignUp']
        
        links = HTMLSelenium.get(self.driver, Tag.to_enum("A"))
        buttons = HTMLSelenium.get(self.driver, Tag.to_enum("BUTTON"))
        es = links + buttons

        auth_model_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "src", "cnn", "auth_model.h5"
        )
        
        model = load_model(auth_model_path)
        potentials = []
        im_width = 64
        im_height = 48

        for e in es:

            try:
                local_img = self._create_local_image_file(e)

                img = image.image_utils.load_img(local_img, target_size=(im_height, im_width))
                img = image.image_utils.img_to_array(img)
                img = img.reshape((1,) + img.shape)
                img = img/255.

                y_prob = model.predict(img)

                for idx, result in enumerate(y_prob[0]):
                    if result * 100 > 95:
                        print(f"Prediction higher than 80 {result} class {classes[idx]}")
                        # Compare
                        ld = label.replace(" ", "").lower()
                        cls = classes[idx].replace(" ", "").lower()
                        if cls == ld:
                            potentials.append({
                                "img": local_img,
                                "score": result * 100,
                                "e": e
                            })
                    else:
                        print(f"{result}")
                    
            except WebDriverException:
                print("continue was never going to compare!")
                pass

        if len(potentials) > 0:
            potential = sorted(potentials, key=itemgetter('score'), reverse=True)  
            return potential[0]['e']

        return None

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
        found_by_cnn = False
        e = self._evaluate_by_selenium(label_data)
        i = None
        if e is None and label_data:
            e = self._evaluate_by_cnn(label_data)
            if e is not None:
                found_by_cnn = True     
        elif e is None and label_data is None:    
            i = None
        
        # CNN or Selenium could not get e
        # try with image_eval. More work!
        if e is None:
            i = self._evaluate_by_image(label_data, e)

        if found_by_cnn:
            Client().create_label_error(label, e)

        if e != None:
            # High Ranking           
            return e

        return None

    def find_by_cnn(self, label: str):
        self.label = label
        self.element = self._evaluate_by_cnn(label)
        return self

    def find_by_label(self, label: str, tag: Union[None, Tag] = None):
        self.label = label
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

        return self

    def method_missing(self, name, *args, **kwargs):
        if name in dir(self.element):
            method = getattr(self.element, name)
            if callable(method):
                try:
                    if self.logging_mode:        
                        Logging().log(self.label, name, self.fl_id, "", self.element, self.driver)
                    return method(*args, **kwargs)
                except Exception as e:
                    # Update Log wil fail
                    print("TEST FAILURE " + e.msg)
                    if self.logging_mode:
                        Logging().log(self.label, name, self.fl_id, e.msg, self.element, self.driver)
            else:
                raise AttributeError(
                    ' %s has not method named "%s" ' % (self.item, name)
                )

        return None

    def screenshot(self, name="tmp.png"):
        self.driver.save_screenshot(name)    