import os
import json
import random
import tempfile
import numpy as np
from flask import Flask, request

from deep_speaker.audio import read_mfcc
from deep_speaker.batcher import sample_from_mfcc
from deep_speaker.constants import SAMPLE_RATE, NUM_FRAMES
from deep_speaker.conv_models import DeepSpeakerModel

np.random.seed(123)
random.seed(123)

print("Loading feature extraction model")
model = DeepSpeakerModel()
model.m.load_weights("models/latest.h5", by_name=True)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_embeddings():
    file = request.files["audio"].read()

    # save temp audio file
    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav")
    tmp_file.write(file)

    # read temp file as spectrogram
    mfcc = sample_from_mfcc(read_mfcc(tmp_file.name, SAMPLE_RATE), NUM_FRAMES)

    # get corresponding embedding
    emb = model.m.predict(np.expand_dims(mfcc, axis=0))
    return json.dumps(emb[0].tolist())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_PORT"))
