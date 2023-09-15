from django import forms
from . import models


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = [
            "document",
        ]
