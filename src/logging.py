import json
import os
import tempfile
from src.client import Client
from src.helper import random_string
from src.file_helper import FileHelper

class Logging:

    @classmethod
    def log(self, label, method, fl_id, error, element, driver):
        resp = Client().logging(label, method, fl_id, error)
        id = json.loads(resp.json())['id']
        
        tmp_image = os.path.join(tempfile.gettempdir(), random_string())
        ss_image  = tmp_image + "_screenshot.png"

        FileHelper.create_image_from_element(tmp_image, element)
        driver.save_screenshot(ss_image)

        Client().upload_logging_image(id, tmp_image, ss_image)

        FileHelper.remove_image(tmp_image)
        FileHelper.remove_image(ss_image)

        return id