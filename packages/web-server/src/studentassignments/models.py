from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
from users.models import User
from assignments.models import Assignment
from clazzes.models import Clazz


class StudentAssignment(ParanoidModel):
    ASSIGNMENT_OPEN = "O"
    ASSIGNMENT_IN_PROGRESS = "I"
    ASSIGNMENT_IN_REVISION = "R"
    ASSIGNMENT_GRADED = "G"
    ASSIGNMENT_STATUS = (
        (
            ASSIGNMENT_OPEN,
            "Open",
        ),  # assignment created by teacher but not started by student
        (ASSIGNMENT_IN_PROGRESS, "In Progress"),  # assignment started by student
        (
            ASSIGNMENT_IN_REVISION,
            "In Revision",
        ),  # assignment ended by student and in revision by teacher
        (ASSIGNMENT_GRADED, "Graded"),  # assignment graded (approved or failed)
    )

    #  Relationships
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # student
    clazz = models.ForeignKey(
        Clazz, on_delete=models.CASCADE, null=True, blank=True
    )  # clazz

    #  Fields
    status = models.TextField(
        max_length=1, choices=ASSIGNMENT_STATUS, default=ASSIGNMENT_STATUS[0][0]
    )
    grade = models.IntegerField(
        blank=True, choices=[(i, i) for i in range(0, 101)], null=True
    )
    final_comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        unique_together = ("assignment", "user")

    def __str__(self):
        return str(self.pk)
