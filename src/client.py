import base64
import json
import requests
from src.helper import strip


class Client:

    api = "http://127.0.0.1:5000"

    @classmethod
    def upload_logging_image(cls, id: str, element_image: str, screenshot: str):

        with open(element_image, "rb") as f:
            im_bytes_1 = f.read()
        im_b64_element = base64.b64encode(im_bytes_1).decode("utf8")

        with open(screenshot, "rb") as f:
            im_bytes_2 = f.read()
        im_b64_screenshot = base64.b64encode(im_bytes_2).decode("utf8")

        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        payload = json.dumps({"image_element": im_b64_element, "image_screenshot": im_b64_screenshot})
        response = requests.post(
            f"{cls.api}/log/{id}/image", data=payload, headers=headers
        )
        return response

    @classmethod
    def upload_image(cls, image_file: str, label: str):

        with open(image_file, "rb") as f:
            im_bytes = f.read()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")

        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        payload = json.dumps({"image": im_b64})
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
        return json.loads(response.json())

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

    @classmethod
    def create_label_error(cls, label: str, element):
        label_resp = json.loads(requests.get(f"{cls.api}/label", params={"label": label}).json())
        errors = {}
        errors_list = []
        if element.get_attribute("text") != label_resp['text']:
            errors_list.append({
                "text": element.get_attribute("text")
            })
        errors['errors'] = errors_list    
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        response = requests.post(
            f"{cls.api}/label/{label_resp['id']}/error", json=errors, headers=headers
        )
        return response

    @classmethod
    def logging(cls, label: str, method: str, fl_id: str, error = ""):
        data = {
            "label": label,
            "method": method,
            "error": error,
            "fl_id": fl_id
        }
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        response = requests.post(f"{cls.api}/log", json=data, headers=headers)
        if response.status_code == 404:
            return None
        return response

    @classmethod
    def get_logging_image(cls, id):
        response = requests.get(f"{cls.api}/logging_image/{id}")
        return response