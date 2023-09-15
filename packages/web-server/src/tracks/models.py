from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
import time
import random

from sessions.models import Session


def random_file_name(instance, filename):
    ext = filename.split(".")[-1]
    filename = "tracks/{}_{}.{}".format(time.time(), random.randint(0, 9999), ext)
    return filename


class Track(ParanoidModel):
    # Choices
    TRACK_TYPING = "T"
    TRACK_FACE = "F"
    TRACK_VOICE = "V"
    TRACK_SCREEN = "S"
    TRACK_TYPE = (
        (TRACK_TYPING, "Typing"),
        (TRACK_FACE, "Face"),
        (TRACK_VOICE, "Voice"),
        (TRACK_SCREEN, "Screen"),
    )

    # Relationships
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)

    # Fields
    type = models.TextField(max_length=1, choices=TRACK_TYPE)
    blob = models.FileField(upload_to=random_file_name, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    is_authenticated = models.BooleanField(default=False)
    quality = models.FloatField(blank=True, default=0)
    confidence = models.FloatField(blank=True, default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
