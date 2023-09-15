FROM python:3.6

# create workdir
RUN mkdir /app
WORKDIR /app

# prepare and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy necessary files
COPY app.py .

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD ["python", "app.py"]