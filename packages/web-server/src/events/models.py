from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel

from users.models import User
from documents.models import Document
from institutions.models import Institution


class Event(ParanoidModel):
    EVENT_PENDING = "P"
    EVENT_ANALYSIS = "A"
    EVENT_CLOSED = "X"
    EVENT_STATUS = (
        (EVENT_PENDING, "Pending",),
        (EVENT_ANALYSIS, "In Analysis"),
        (EVENT_CLOSED, "Closed"),
    )

    EVENT_TRACK_TYPING_FAILURE = 1
    EVENT_TYPES = ((EVENT_TRACK_TYPING_FAILURE, "Typing Verification Failure"),)

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True
    )

    #  Fields
    event_type = models.TextField(max_length=1, choices=EVENT_TYPES)
    status = models.TextField(max_length=1, choices=EVENT_STATUS, default=EVENT_PENDING)
    quality = models.FloatField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["status", "-id"]

    def __str__(self):
        return str(self.pk)
