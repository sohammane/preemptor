docker build -t textencoder .
docker run --gpus all --rm -it -p 127.0.0.1:5002:5002 textencoder