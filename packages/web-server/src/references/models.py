from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
from documents.models import Document


class Reference(ParanoidModel):
    # Relationships
    documents = models.ManyToManyField(Document, related_name="references", blank=True)

    #  Fields
    name = models.TextField()
    year = models.TextField()
    authors = models.TextField()
    journal = models.TextField(blank=True)
    location = models.TextField(blank=True)
    url = models.TextField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
