from selenium import webdriver
from PIL import Image as Img
from src.file_helper import FileHelper
from src.html import HTML, Tag
import os
import pytesseract as pt
import cv2

class ImageText:

    tmp_image = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "data", "images", "image.png"
    )

    def __init__(self, driver: webdriver):
        self.driver = driver

    def find_by_tag(self, tag: Tag, text_search: str):
        es = HTML.get(self.driver, tag)
        element = None
        for e in es:
            try:

                img_file = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "data",
                    "images",
                    f"{text_search.lower()}.png",
                )

                tmp = FileHelper.create_image_temp(self.tmp_image, e)
                img = cv2.imread(tmp)
                
                (h, w) = img.shape[:2]
                img = cv2.resize(img, (w*3, h*3))
                gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thr = cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                img_text = pt.image_to_string(thr).strip()

                if img_text.lower() == text_search.lower():
                    element = e
                    FileHelper.save_image(self.tmp_image, img_file)
                    break

            except Exception as ex:
                print(ex)
                pass
        return element
