import os
import json
import random
import numpy as np
from flask import Flask, request
from sentence_transformers import SentenceTransformer

np.random.seed(123)
random.seed(123)

print("Loading text embedding model")
model = SentenceTransformer("xlm-r-distilroberta-base-paraphrase-v1")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_embeddings():
    text = request.form.get("text")
    emb = model.encode(text).tolist()
    return json.dumps(emb)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_PORT"))
