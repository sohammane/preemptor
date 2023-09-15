from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
from users.models import User
from documents.models import Document


class Session(ParanoidModel):
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)

    # Fields
    is_authenticated = models.BooleanField(default=False)
    quality = models.FloatField(blank=True, default=0)
    confidence = models.FloatField(blank=True, default=0)

    has_typing = models.BooleanField(default=False)
    has_face = models.BooleanField(default=False)
    has_voice = models.BooleanField(default=False)
    has_screen = models.BooleanField(default=False)

    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
