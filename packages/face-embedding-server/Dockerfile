FROM tensorflow/tensorflow:1.7.0-gpu-py3

# create workdir
RUN mkdir /app
WORKDIR /app

# prepare and install requirements
RUN apt-get update && apt-get install -y git
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN git clone https://github.com/bryanoliveira/facenet


# copy necessary files
COPY ./models ./models
COPY app.py .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD ["python", "app.py"]