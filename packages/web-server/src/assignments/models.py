from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel

from users.models import User


class Assignment(ParanoidModel):
    ASSIGNMENT_DRAFT = "D"
    ASSIGNMENT_OPEN = "O"
    ASSIGNMENT_IN_PROGRESS = "I"
    ASSIGNMENT_CLOSED = "C"
    ASSIGNMENT_STATUS = (
        (ASSIGNMENT_DRAFT, "Draft"),  # assignment is being created by teacher
        (
            ASSIGNMENT_OPEN,
            "Open",
        ),  # assignment created by teacher but not started by student
        (ASSIGNMENT_IN_PROGRESS, "In Progress"),  # assignment started by student
        (
            ASSIGNMENT_CLOSED,
            "Closed",
        ),  # assignment ended by student and in revision by teacher
    )

    #  Relationships
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)  # teacher

    #  Fields
    name = models.TextField()  # required
    description = models.TextField(blank=True)
    status = models.TextField(
        max_length=1, choices=ASSIGNMENT_STATUS, default=ASSIGNMENT_STATUS[0][0]
    )
    final_comment = models.TextField(blank=True)
    due_at = models.DateTimeField(
        null=True, blank=True
    )  # due date for statuses "Open" and "In progress" (teacher can update it later)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.pk)

