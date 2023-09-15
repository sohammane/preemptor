from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
from assignments.models import Assignment
from studentassignments.models import StudentAssignment
from users.models import User


class Document(ParanoidModel):
    #  Relationships
    assignment = models.ForeignKey(
        Assignment, on_delete=models.SET_NULL, null=True, blank=True
    )
    studentassignment = models.ForeignKey(
        StudentAssignment, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    #  Fields
    name = models.TextField(blank=True)
    data = models.TextField(blank=True)
    raw_data = models.TextField(blank=True, null=True)
    has_template = models.BooleanField(default=False)
    requires_face = models.BooleanField(default=False)
    requires_voice = models.BooleanField(default=False)
    requires_screen = models.BooleanField(default=False)
    pasted_chars = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]
        # one user can have only one document per studentassignment and vice versa
        unique_together = ("studentassignment", "user")

    def __str__(self):
        return str(self.pk)
