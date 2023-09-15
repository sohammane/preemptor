from django import forms
from . import models


class VoucherForm(forms.ModelForm):
    class Meta:
        model = models.Voucher
        fields = ["name", "code", "institution", "max_uses"]
