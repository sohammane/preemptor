from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import urllib3
from urllib import parse
import json
import base64
import os
import io
import uuid
from datetime import datetime
from elasticsearch import Elasticsearch
from PIL import Image
import cv2
import numpy as np

from . import utils
from .models import Track
from events.models import Event

from sessions.utils import get_last_session, update_session

es = Elasticsearch([{"host": os.environ.get("ELASTICSEARCH_HOST")}])


def save_img_track(
    request, imgbuf, embedding=None, authenticated=True, confidence=0, quality=0
):
    # log track
    # - get image buffer
    _, buffer = cv2.imencode(".jpg", imgbuf)
    io_buf = io.BytesIO(buffer)
    # - get active session
    session = get_last_session(request.user)
    track = Track(
        session=session,
        type=Track.TRACK_FACE,
        blob=File(io_buf, name="image.jpg"),
        metadata=embedding,
        is_authenticated=authenticated,
        quality=quality,
        confidence=confidence,
    )
    track.save()
    update_session(session, track_type=Track.TRACK_FACE)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def register_face(request):
    # receive image
    if request.FILES.get("image") is not None:
        imgbuf = request.FILES.get("image").read()
        imgbuf = np.fromstring(imgbuf, np.uint8)
        imgbuf = cv2.imdecode(imgbuf, cv2.IMREAD_ANYCOLOR)
    elif request.POST.get("image") is not None:
        imgbuf = request.POST.get("image").split(",")[1]
        imgbuf = io.BytesIO(base64.b64decode(imgbuf))
        imgbuf = Image.open(imgbuf)
        imgbuf = np.array(imgbuf)
        imgbuf = cv2.cvtColor(imgbuf, cv2.COLOR_BGR2RGB)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # detect and crop face in image
    faces = utils.crop_faces(imgbuf)
    if len(faces) == 0:
        return Response(
            {"detail": "No faces found."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
    elif len(faces) > 1:
        return Response(
            {"detail": "Multiple faces found."}, status=status.HTTP_409_CONFLICT
        )
    face = faces[0]

    # send image to facenet and receive embedding
    http = urllib3.PoolManager()
    serialized_data = http.request(
        "POST", os.environ.get("FACE_SERVER"), fields={"image": ("image", face)},
    )
    # print(serialized_data.data)
    embedding = None
    try:
        embedding = json.loads(serialized_data.data.decode("utf-8"))
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Embedding parse error."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )

    # save embedding to elasticsearch
    es_entry = {
        "embedding": embedding,
        "user_id": request.user.id,
        "datetime_created": int(
            datetime.now().timestamp() * 1000
        ),  # datetime, in milliseconds since epoch
    }
    res = es.index(
        index=os.environ.get("FACE_EMBEDDING_INDEX"), body=es_entry, refresh=True
    )

    request.user.has_face = True
    request.user.save()

    return Response({"result": res["result"]})


@api_view(("DELETE",))
@renderer_classes((JSONRenderer,))
@login_required
def delete_faces(request):
    # delete this user's face embeddings
    query = {"query": {"match": {"user_id": request.user.id}}}
    res = es.delete_by_query(
        index=os.environ.get("FACE_EMBEDDING_INDEX"), body=query, refresh=True
    )
    return Response({"deleted": res["deleted"]})


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def log_face(request):
    # receive image
    if request.FILES.get("image") is not None:
        imgbuf = request.FILES.get("image").read()
        imgbuf = np.fromstring(imgbuf, np.uint8)
        imgbuf = cv2.imdecode(imgbuf, cv2.IMREAD_ANYCOLOR)
    elif request.POST.get("image") is not None:
        imgbuf = request.POST.get("image").split(",")[1]
        imgbuf = io.BytesIO(base64.b64decode(imgbuf))
        imgbuf = Image.open(imgbuf)
        imgbuf = np.array(imgbuf)
        imgbuf = cv2.cvtColor(imgbuf, cv2.COLOR_BGR2RGB)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # detect and crop face in image
    faces = utils.crop_faces(imgbuf)
    if len(faces) == 0:
        save_img_track(
            request, imgbuf,
        )
        return Response(
            {"detail": "No faces found."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
    elif len(faces) > 1:
        save_img_track(
            request, imgbuf, quality=1,
        )
        return Response(
            {"detail": "Multiple faces found."}, status=status.HTTP_409_CONFLICT
        )
    face = faces[0]

    # send image to facenet and receive embedding
    http = urllib3.PoolManager()
    serialized_data = http.request(
        "POST", os.environ.get("FACE_SERVER"), fields={"image": ("image.jpg", face)},
    )
    embedding = None
    try:
        embedding = json.loads(serialized_data.data.decode("utf-8"))
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Embedding parse error."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )

    if request.user.has_face:
        # check best matching users with elasticsearch
        query = {
            "_source": ["user_id", "datetime_created"],
            "min_score": 1.9,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": embedding},
                    },
                }
            },
        }
        res = es.search(
            body=query, index=os.environ.get("FACE_EMBEDDING_INDEX"), size=5
        )  # limit top 5 results
        matches = [
            {
                "id": hit["_id"],
                "user_id": hit["_source"]["user_id"],
                "score": hit["_score"],
            }
            for hit in res["hits"]["hits"]
        ]
        same_user = request.user.id in [match["user_id"] for match in matches]

        authenticated = res["hits"]["max_score"] is not None
        save_img_track(
            request,
            imgbuf,
            embedding=embedding,
            authenticated=authenticated,
            confidence=res["hits"]["max_score"] - 1 if authenticated else 0,
            quality=1 if authenticated else 0,
        )

        return Response(
            {
                "is_match": same_user,
                "max_score": res["hits"]["max_score"],
                "matches": matches,
            }
        )
    else:
        save_img_track(
            request,
            imgbuf,
            embedding=embedding,
            authenticated=0,
            confidence=0,
            quality=1,
        )
        return Response({"is_match": False, "max_score": 0, "matches": []})


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def register_voice(request):
    # receive audio
    if request.FILES.get("audio") is not None:
        audio = request.FILES.get("audio").read()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # send audio to deepspeaker and receive embedding
    http = urllib3.PoolManager()
    serialized_data = http.request(
        "POST", os.environ.get("VOICE_SERVER"), fields={"audio": ("audio.wav", audio)},
    )
    embedding = None
    try:
        embedding = json.loads(serialized_data.data.decode("utf-8"))
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Embedding parse error."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )

    # save embedding to elasticsearch
    es_entry = {
        "embedding": embedding,
        "user_id": request.user.id,
        "datetime_created": int(
            datetime.now().timestamp() * 1000
        ),  # datetime, in milliseconds since epoch
    }
    res = es.index(
        index=os.environ.get("VOICE_EMBEDDING_INDEX"), body=es_entry, refresh=True
    )

    request.user.has_voice = True
    request.user.save()

    return Response({"result": res["result"]})


@api_view(("DELETE",))
@renderer_classes((JSONRenderer,))
@login_required
def delete_voices(request):
    # delete this user's voice embeddings
    query = {"query": {"match": {"user_id": request.user.id}}}
    res = es.delete_by_query(
        index=os.environ.get("VOICE_EMBEDDING_INDEX"), body=query, refresh=True
    )
    return Response({"deleted": res["deleted"]})


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def log_voice(request):
    # receive audio
    if request.FILES.get("audio") is not None:
        audio = request.FILES.get("audio").read()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    io_buf = io.BytesIO(audio)  # to be saved locally

    # send audio to deepspeaker and receive embedding
    http = urllib3.PoolManager()
    serialized_data = http.request(
        "POST", os.environ.get("VOICE_SERVER"), fields={"audio": ("audio.wav", audio)},
    )
    embedding = None
    try:
        embedding = json.loads(serialized_data.data.decode("utf-8"))
    except Exception as e:
        print(e)
        return Response(
            {"detail": "Embedding parse error."}, status=status.HTTP_406_NOT_ACCEPTABLE
        )

    # get active session
    session = get_last_session(request.user)

    if request.user.has_voice:
        # check best matching users with elasticsearch
        query = {
            "_source": ["user_id", "datetime_created"],
            "min_score": 1.5,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": embedding},
                    },
                }
            },
        }
        res = es.search(
            body=query, index=os.environ.get("VOICE_EMBEDDING_INDEX"), size=5
        )  # limit top 5 results
        matches = [
            {
                "id": hit["_id"],
                "user_id": hit["_source"]["user_id"],
                "score": hit["_score"],
            }
            for hit in res["hits"]["hits"]
        ]
        same_user = request.user.id in [match["user_id"] for match in matches]

        # log track
        authenticated = res["hits"]["max_score"] is not None
        confidence = (
            res["hits"]["max_score"] - 1 if authenticated else 0
        )  # confidence E (0, 1)
        track = Track(
            session=session,
            type=Track.TRACK_VOICE,
            blob=File(io_buf, name="audio.wav"),
            metadata=embedding,
            is_authenticated=authenticated,
            quality=1 if authenticated else 0,
            confidence=confidence,
        )
        track.save()
        update_session(session, track_type=Track.TRACK_VOICE)

        return Response(
            {
                "is_match": same_user,
                "max_score": res["hits"]["max_score"],
                "matches": matches,
            }
        )
    else:
        track = Track(
            session=session,
            type=Track.TRACK_VOICE,
            blob=File(io_buf, name="audio.wav"),
            metadata=embedding,
            is_authenticated=0,
            quality=1,
            confidence=0,
        )
        track.save()
        update_session(session, track_type=Track.TRACK_VOICE)
        return Response({"is_match": False, "max_score": 0, "matches": []})


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def log_typing(request):
    # get request content (typing pattern)
    pattern = r"{}".format(request.POST.get("pattern"))
    text = request.POST.get("text")
    ip = utils.get_client_ip(request)
    userAgent = request.META.get("HTTP_USER_AGENT")
    session = get_last_session(request.user)  # get active session
    trainSession = str(uuid.uuid4().hex)

    payload = {
        "tenantId": "pre468029",
        "userId": request.user.id,
        "sessionId": session.id if session else trainSession,
        "userAgent": userAgent,
        "ip": ip,
        # score, confidence & is_trained
        "reportFlags": 259,
        # force train if not in a writing session (which will be ended manually)
        "operatorFlags": 8 if not session else 1,
        "timing": pattern,
    }
    payload = parse.urlencode(
        payload, quote_via=parse.quote, safe="()", encoding="ascii"
    )

    # instantiate request object
    http = urllib3.PoolManager()
    serialized_data = http.request(
        "POST",
        os.environ.get("BEHAVIOSENSE_SERVER") + "/BehavioSenseAPI/GetReport",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        body=payload,
        encode_multipart=False,
    )
    data = json.loads(serialized_data.data.decode("utf-8"))

    # finalize train session
    if not session:
        http = urllib3.PoolManager()
        http.request_encode_body(
            "POST",
            os.environ.get("BEHAVIOSENSE_SERVER") + "/BehavioSenseAPI/FinalizeSession",
            fields={"tenantId": "pre468029", "sessionId": trainSession},
            encode_multipart=False,
        )

    # log track
    track = Track(
        session=session,
        type=Track.TRACK_TYPING,
        data=pattern,
        metadata=text,
        is_authenticated="score" in data,
        quality=data["confidence"] if "confidence" in data else 0,
        confidence=data["score"] if "score" in data else 0,
    )
    track.save()
    update_session(session, track_type=Track.TRACK_TYPING)

    if (
        track.is_authenticated
        and track.quality > 0.7
        and track.confidence < 0.4
        and session is not None
    ):
        event = Event(
            user=request.user,
            document=session.document,
            type=Event.EVENT_TRACK_TYPING_FAILURE,
            quality=track.quality,
            confidence=track.confidence,
        )
        event.save()

    if (
        track.is_authenticated
        and track.quality > 0.7
        and track.confidence > 0.8
        and session
    ):
        http = urllib3.PoolManager()
        http.request_encode_body(
            "POST",
            os.environ.get("BEHAVIOSENSE_SERVER") + "/BehavioSenseAPI/ForceTrain",
            fields={
                "tenantId": "pre468029",
                "userId": request.user.id,
                "sessionId": session.id,
                "reason": "Score is satisfactory.",
            },
            encode_multipart=False,
        )

    if not request.user.has_typing:
        request.user.has_typing = True
        request.user.save()

    return Response(data)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def log_screen(request):
    # receive image
    if request.FILES.get("image") is not None:
        imgbuf = request.FILES.get("image").read()
        imgbuf = np.fromstring(imgbuf, np.uint8)
        imgbuf = cv2.imdecode(imgbuf, cv2.IMREAD_ANYCOLOR)
    elif request.POST.get("image") is not None:
        imgbuf = request.POST.get("image").split(",")[1]
        imgbuf = io.BytesIO(base64.b64decode(imgbuf))
        imgbuf = Image.open(imgbuf)
        imgbuf = np.array(imgbuf)
        imgbuf = cv2.cvtColor(imgbuf, cv2.COLOR_BGR2RGB)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # log track
    # - get image buffer
    _, buffer = cv2.imencode(".jpg", imgbuf)
    io_buf = io.BytesIO(buffer)
    # - get active session
    session = get_last_session(request.user)
    track = Track(
        session=session,
        type=Track.TRACK_SCREEN,
        blob=File(io_buf, name="image.jpg"),
        is_authenticated=True,
        quality=1,
        confidence=1,
    )
    track.save()
    update_session(session, track_type=Track.TRACK_SCREEN)

    return Response({"success": True})

