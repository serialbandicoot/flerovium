from flask import Flask, abort, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image

import json
import os
import base64
import io

from helper_logging import HelperLogging
from helper import image_path, logging_image_path
from helper_db import HelperDB
from cnn import CNN
from helper_cnn import HelperCNN

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Flerovium API"

@app.route("/label/<id>/error", methods=["POST"])
def error(id):
    return json.dumps(json.dumps(HelperDB().put_label(id, request.json)))

@app.route("/label/<id>/error", methods=["PUT"])
def error_delete(id): 
    key = request.json['key']
    label = HelperDB().get_label(id)   
    del label['errors'][0][key]
    return json.dumps(json.dumps(HelperDB().put_label(id, label)))

@app.route("/labelce", methods=["POST"])
def post_test():
    data = {
                "label": request.values["label"],
                "image_name": request.values["image_name"],
                "tag_name": request.values["tag_name"],
                "accessible_name": request.values["accessible_name"],
                "text": request.values["text"],
                "e_id": request.values["e_id"],
                "name": request.values["name"],
                "placeholder": request.values["placeholder"],
                "class": request.values["class"],
            }
    HelperDB().post_label(data)       

    # convert it into bytes
    img_bytes = base64.b64decode(request.values["image_b64"].split(',')[1])

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    img_path = os.path.join(image_path(), request.values["image_name"])
    if os.path.exists(img_path):
        os.remove(img_path)
    img.save(img_path, format="png")

    return {"status": "ok"}

@app.route("/labels", methods=["GET"])
def labels():
    return json.dumps(HelperDB().get_all_labels())


@app.route("/label/<id>", methods=["GET"])
def label_by_id_get(id):
    return json.dumps(json.dumps(HelperDB().get_label(id)))


@app.route("/label", methods=["GET"])
def label_by_label_get():
    args = request.args
    label = args.get("label")
    label_data = HelperDB().get_by_label(label)
    if label_data is None:
        abort(404)
    return json.dumps(json.dumps(label_data))


@app.route("/label/<id>", methods=["DELETE"])
def label_delete(id):
    return json.dumps(json.dumps(HelperDB().delete_label(id)))


@app.route("/label", methods=["POST"])
def label_post():
    return json.dumps(json.dumps(HelperDB().post_label(request.json)))


@app.route("/label/<id>", methods=["PUT"])
def label_put(id):
    return json.dumps(json.dumps(HelperDB().put_label(id, request.json)))


@app.route("/image", methods=["GET"])
def image_get():
    args = request.args
    name = args.get("name")
    img = os.path.join(image_path(), name)
    if os.path.exists(img):
        return send_file(img, mimetype="image/png")
    else:
        abort(404)


@app.route("/image/<label>", methods=["POST"])
def image_post(label):
    if not request.json or "image" not in request.json:
        abort(400)

    # get the base64 encoded string
    im_b64 = request.json["image"]

    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode("utf-8"))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    img_path = os.path.join(image_path(), f"{label}.png")
    if os.path.exists(img_path):
        os.remove(img_path)
    img.save(img_path, format="png")

    return ("", 204)

@app.route("/logging", methods=["GET"])
def logging_get():
    return json.dumps(HelperLogging().get_logs())

@app.route("/log", methods=["POST"])
def logging_post():
    id = HelperLogging().post_log(request.json)
    id = {
        "id": id
    }
    return json.dumps(json.dumps(id))

@app.route("/log/<id>/image", methods=["POST"])
def logging_image_post(id):
    if not request.json or "image_element" not in request.json:
        abort(400)

    # get the base64 encoded string
    im_b64_element = request.json["image_element"]
    im_b64_screenshot = request.json["image_screenshot"]

    # convert it into bytes
    img_bytes_1 = base64.b64decode(im_b64_element.encode("utf-8"))
    img_bytes_2 = base64.b64decode(im_b64_screenshot.encode("utf-8"))

    # convert bytes data to PIL Image object
    img_1 = Image.open(io.BytesIO(img_bytes_1))
    img_2 = Image.open(io.BytesIO(img_bytes_2))

    img_path_1 = os.path.join(logging_image_path(), f"{id}_element.png")
    img_path_2 = os.path.join(logging_image_path(), f"{id}_screenshot.png")

    if os.path.exists(img_path_1):
        os.remove(img_path_1)
    img_1.save(img_path_1, format="png")

    if os.path.exists(img_path_2):
        os.remove(img_path_2)
    img_2.save(img_path_2, format="png")

    return ("", 204)

@app.route("/logging_image", methods=["GET"])
def logging_image_get():
    args = request.args
    id = args.get("id")
    el = args.get("element")
    ss = args.get("screenshot") #Some Work!
    
    if el == "true":
        img = os.path.join(logging_image_path(), f"{id}_element.png")
    else:
        img = os.path.join(logging_image_path(), f"{id}_screenshot.png")

    if os.path.exists(img):
        return send_file(img, mimetype="image/png")
    else:
        abort(404)

@app.route("/log/fl/<id>", methods=["GET"])
def logging_by_fl_id(id):
    return json.dumps(HelperLogging().get_logs_by_fl_id(id))

@app.route("/predict/<id>", methods=["GET"])
def predict(id):
    return json.dumps(CNN().predict(id))

@app.route("/generate")
def generate():
    return json.dumps(HelperCNN().generate_button())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
