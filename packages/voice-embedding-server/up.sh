docker build -t voiceencoder .
docker run --gpus all --rm -it -p 127.0.0.1:5001:5001 voiceencoder