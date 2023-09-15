from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
import uuid

from users.models import User
from documents.models import Document


class Merit(ParanoidModel):
    # Choices
    QUANTITIES = [10, 10, 20, 10]
    TYPE_REGISTER = 0
    TYPE_PROFILE_COMPLETE = 1
    TYPE_ASSIGNMENT_SUBMIT = 2
    TYPE_ASSIGNMENT_GRADE_75 = 3
    MERIT_TYPE = (
        (TYPE_REGISTER, "Registered"),
        (TYPE_PROFILE_COMPLETE, "Completed profile"),
        (TYPE_ASSIGNMENT_SUBMIT, "Submitted assignment"),
        (TYPE_ASSIGNMENT_GRADE_75, "Assignment graded above 75"),
    )

    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #  Fields
    merit_type = models.TextField(max_length=1, choices=MERIT_TYPE)
    quantity = models.IntegerField(default=10)

    # optional references
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)
