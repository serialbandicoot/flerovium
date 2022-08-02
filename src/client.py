import base64
import json
import requests
from src.helper import strip


class Client:

    api = "http://127.0.0.1:5000"

    @classmethod
    def upload_image(cls, image_file: str, label: str):

        with open(image_file, "rb") as f:
            im_bytes = f.read()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")

        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        payload = json.dumps({"image": im_b64, "other_key": "value"})
        response = requests.post(
            f"{cls.api}/image/{label}", data=payload, headers=headers
        )
        try:
            data = response.json()
            print(data)
        except requests.exceptions.RequestException:
            print(response.text)

    @classmethod
    def get_image(cls, label):
        response = requests.get(f"{cls.api}/image/{label}")
        return response

    @classmethod
    def get_by_label(cls, label):
        response = requests.get(f"{cls.api}/label", params={"label": label})
        if response.status_code == 404:
            return None
        return response.json()

    @classmethod
    def save_data(cls, label, element):
        data = {
            "label": label,
            "image_name": f"{label}.png",
            "tag_name": element.tag_name,
            "accessible_name": strip(element.accessible_name),
            "text": strip(element.text),
            "e_id": strip(element.get_attribute("id")),
            "name": strip(element.get_attribute("name")),
            "placeholder": strip(element.get_attribute("placeholder")),
            "class": strip(element.get_attribute("class")),
        }
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        response = requests.post(f"{cls.api}/label", json=data, headers=headers)
        if response.status_code == 404:
            return None
        return response

    @classmethod
    def get_raw_image(cls, image_name: str):
        return requests.get(
            f"{cls.api}/image", params={"name": image_name}, stream=True
        )
