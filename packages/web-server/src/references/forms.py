from django import forms
from . import models


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = models.Reference
        fields = ["documents", "name", "year", "authors", "journal", "url", "location"]
