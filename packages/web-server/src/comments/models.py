from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel

from documents.models import Document
from users.models import User


class Comment(ParanoidModel):
    # Relationships
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    #  Fields
    data = models.TextField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return str(self.pk)
