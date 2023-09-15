import math
import os
from django.utils import timezone
from django.db.models import Avg, Count
import urllib3

from .models import Session
from tracks.models import Track


def get_last_session(user):
    session = Session.objects.filter(user=user, ended_at=None)
    return session[0] if len(session) > 0 else None


def end_session(session):
    if not session:
        return
    session.ended_at = timezone.now()
    session.save()

    # end behaviosec session
    http = urllib3.PoolManager()
    http.request_encode_body(
        "POST",
        os.environ.get("BEHAVIOSENSE_SERVER") + "/BehavioSenseAPI/FinalizeSession",
        fields={"tenantId": "pre468029", "sessionId": session.id},
        encode_multipart=False,
    )


def update_session(session, track_type=None):
    if session is None:
        return

    if track_type == Track.TRACK_TYPING:
        session.has_typing = True
    elif track_type == Track.TRACK_FACE:
        session.has_face = True
    elif track_type == Track.TRACK_VOICE:
        session.has_voice = True
    elif track_type == Track.TRACK_SCREEN:
        session.has_screen = True

    qs = Track.objects.filter(session=session, type=Track.TRACK_TYPING)

    quality = qs.aggregate(quality=Avg("quality"))
    confidence = qs.filter(quality__gt=0.5).aggregate(
        confidence=Avg("confidence"), cnt=Count("id")
    )

    if quality["quality"]:
        session.quality = quality["quality"]
    if confidence["confidence"]:
        # distrust sessions where quality authentications are less than 1 examples
        session.confidence = confidence["confidence"] * math.tanh(confidence["cnt"] / 1)
        if confidence["confidence"] > 0:
            session.is_authenticated = True
    session.save()
