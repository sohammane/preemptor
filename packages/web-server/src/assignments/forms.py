from django import forms
from . import models


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = [
            "name",
            "description",
            "user",
            "status",
            "final_comment",
            "datetime_due",
        ]

