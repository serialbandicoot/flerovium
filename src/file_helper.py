import os
from src.client import Client


class FileHelper:
    @staticmethod
    def move_file(before: str, after: str) -> str:
        if os.path.exists(before):
            os.rename(before, after)

    @staticmethod
    def create_image_from_element(file: str, element):
        f = open(file, "wb")
        f.write(element.screenshot_as_png)
        f.close()

    @staticmethod
    def save_image(before: str, after: str):
        if os.path.exists(after):
            os.remove(after)
        os.rename(before, after)

    @staticmethod
    def remove_image(file: str):
        if os.path.exists(file):
            os.remove(file)
