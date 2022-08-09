import os
import tempfile

import cv2
import pytesseract as pt
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from src.client import Client
from src.file_helper import FileHelper
from src.helper import random_string
from src.html_selenium import HTMLSelenium, Tag


class ImageText:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def find_by_tag(self, tag: Tag, label: str, save_file=False, db_save=True):
        es = HTMLSelenium.get(self.driver, tag)
        element = None

        if save_file is False:
            img_file_name = label.replace(" ", "_")
        else:
            img_file_name = save_file

        for e in es:
            try:
                tmp_image = os.path.join(tempfile.gettempdir(), random_string())
                img_text = self._image_text(e, tmp_image)

                if img_text.lower() == label.lower():
                    element = e

                    self._persist_data(
                        label, save_file, db_save, img_file_name, e, tmp_image
                    )

                    FileHelper.remove_image(tmp_image)  # Cleanup
                    break

                FileHelper.remove_image(tmp_image)  # Cleanup

            except WebDriverException as exe:
                exe
                pass
        
        if element is None and tag is Tag.INPUT:
            for e in es:
                try:
                    ep = e.find_element(By.XPATH, "..")
                    tmp_image = os.path.join(tempfile.gettempdir(), random_string())
                    img_text = self._image_text(ep, tmp_image)

                    if img_text.lower() == label.lower():
                        element = e

                        self._persist_data(label, save_file, db_save, img_file_name, e, tmp_image)

                        FileHelper.remove_image(tmp_image)  # Cleanup
                        break

                    FileHelper.remove_image(tmp_image)  # Cleanup

                except WebDriverException as exe:
                    exe
                    pass

        return element

    def _persist_data(self, label, save_file, db_save, img_file_name, e, tmp_image):
        if save_file is False:
            Client().upload_image(tmp_image, img_file_name)
        else:
            print(save_file)
            FileHelper.move_file(tmp_image, save_file)

        if db_save:
            Client().save_data(label, e)

    def _image_text(self, e, tmp_image):
        FileHelper.create_image_from_element(tmp_image, e)
        img = cv2.imread(tmp_image)

        (h, w) = img.shape[:2]
        img = cv2.resize(img, (w * 3, h * 3))
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr = cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        img_text = pt.image_to_string(thr).strip()
        return img_text
