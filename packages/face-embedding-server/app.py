import os
import tensorflow as tf
import json
from flask import Flask, request
import numpy as np
import cv2

from facenet.src import facenet


sess = tf.Session()

print("Loading feature extraction model")
facenet.load_model("models/latest/20180402-114759.pb")

# Get input and output tensors
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_embeddings():
    file = request.files["image"]
    npimg = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = facenet.crop(img, False, 160)
    feed_dict = {images_placeholder: [img], phase_train_placeholder: False}
    emb = sess.run(embeddings, feed_dict=feed_dict)
    return json.dumps(emb[0].tolist())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_PORT"))
