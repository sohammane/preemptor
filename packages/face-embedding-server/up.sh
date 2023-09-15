docker build -t facenet .
docker run --gpus all --rm -it -p 127.0.0.1:5000:5000 facenet