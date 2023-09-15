import os
import base64
import json
import urllib3
import cv2
import numpy as np

classifier = cv2.CascadeClassifier("./tracks/haarcascade_frontalface_default.xml")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def square_img(img):
    if img.shape[0] > img.shape[1]:
        d = int((img.shape[0] - img.shape[1]) / 2)
        m = img.shape[1]
        return img[d : m + d, :]
    else:
        d = int((img.shape[1] - img.shape[0]) / 2)
        m = img.shape[0]
        return img[:, d : m + d]


def crop_faces(img):
    img = square_img(img)
    img = cv2.resize(img, (500, 500))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = classifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    cropped_faces = []
    for (x, y, w, h) in faces:
        face = img[y : y + h, x : x + w]
        face_str = cv2.imencode(".png", face)[1].tostring()
        cropped_faces.append(face_str)
        # cv2.imwrite("f{}.png".format(len(cropped_faces)), face)

    return cropped_faces
