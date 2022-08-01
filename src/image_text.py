from ast import expr
from cProfile import label
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from PIL import Image as Img
from src.file_helper import FileHelper
from src.html import HTML, Tag
from src.db import DB
import os
import pytesseract as pt
import cv2


class ImageText:

    tmp_image = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "data", "images", "image.png"
    )

    def __init__(self, driver: webdriver):
        self.driver = driver

    def find_by_tag(self, tag: Tag, label: str):
        es = HTML.get(self.driver, tag)
        element = None
        for e in es:
            img_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "..",
                "data",
                "images",
                f"{label}.png",
            )
            try:
                tmp = FileHelper.create_image_temp(self.tmp_image, e)
                img = cv2.imread(tmp)

                (h, w) = img.shape[:2]
                img = cv2.resize(img, (w * 3, h * 3))
                gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thr = cv2.threshold(
                    gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                )[1]

                img_text = pt.image_to_string(thr).strip()

                if img_text.lower() == label.lower():
                    element = e
                    FileHelper.save_image(self.tmp_image, img_file)
                    DB().save_data(label, e)
                    break
            except WebDriverException as exe:
                exe
                pass

        return element
