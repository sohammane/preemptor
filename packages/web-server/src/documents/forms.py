from django import forms
from . import models


class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = [
            "assignment",
            "studentassignment",
            "name",
            "data",
            "raw_data",
            "requires_face",
            "requires_voice",
            "requires_screen",
            "pasted_chars",
        ]
