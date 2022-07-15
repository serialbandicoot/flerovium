import os
import pytesseract as pt
from PIL import Image as Img
from src.html import HTML, Tag


class Flerovium:

    TMP_IMAGE = f"images/image.png"

    def __init__(self, driver):
        self.driver = driver

    def _create_image_temp(self, element) -> str:
        if os.path.exists(self.TMP_IMAGE):
            os.remove(self.TMP_IMAGE)
        f = open(self.TMP_IMAGE, "wb")
        f.write(element.screenshot_as_png)
        f.close()
        return self.TMP_IMAGE

    def _save_image(self, name: str):
        i = f"images/{name}.png"
        if os.path.exists(i):
            os.remove(i)
        os.rename(self.TMP_IMAGE, i)

    def _find_by_tag(self, tag: Tag, text_search: str):
        es = HTML.get(self.driver, tag)
        element = None
        for e in es:
            try:
                tmp = self._create_image_temp(e)
                img = Img.open(tmp)
                img_text = pt.image_to_string(img).strip()
                if img_text.lower() == text_search.lower():
                    element = e
                    self._save_image(text_search.lower())
                    break

            except Exception as ex:
                print(ex)
                pass
        return element

    def find_by_label(self, text_search: str):
        byA = self._find_by_tag(Tag.A, text_search)
        return byA
