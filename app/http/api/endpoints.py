from flask import Flask, abort, request, send_file
from flask_cors import CORS
from src.db import DB
import json
import os

images_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "..",
    "..",
    "data",
    "images"
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Flerovium API"

@app.route("/labels", methods=['GET'])
def labels():
    return json.dumps(DB().get_all_labels())
     
@app.route("/label/<id>", methods=['GET'])
def label_get(id):
    return json.dumps(json.dumps(DB().get_label(id)))

@app.route("/label/<id>", methods=['DELETE'])
def label_delete(id):
    return json.dumps(json.dumps(DB().delete_label(id)))

@app.route("/label/<id>", methods=['PUT'])
def label_put(id):    
    return json.dumps(json.dumps(DB().put_label(id, request.json)))

@app.route("/image", methods=['GET'])
def image():
    args = request.args
    name = args.get('name')
    img = os.path.join(images_path, name)
    if os.path.exists(img):
        return send_file(img, mimetype='image/png')
    else:
        abort(404)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
