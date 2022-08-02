from flask import Flask, abort, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image

import json
import os
import base64
import io

from app.http.api.helper import image_path
from app.http.api.helper_db import HelperDB

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Flerovium API"


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
    return jsonify(label_data)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
