from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
import uuid

from institutions.models import Institution
from users.models import User


def gen_code():
    # truncation may lead to collisions but we filter by institution when searching for a clazz
    # which dramatically decreases probability - n/4.294.967.296
    return str(uuid.uuid4())[:8]


class Clazz(ParanoidModel):
    # Relationships
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True)
    owners = models.ManyToManyField(
        User, related_name="oclazzes", blank=True
    )  # professors
    users = models.ManyToManyField(User, related_name="clazzes", blank=True)  # students

    #  Fields
    code = models.TextField(default=gen_code, editable=False)
    name = models.TextField()
    description = models.TextField()

    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
