from django.db import models
from django.urls import reverse
from django_paranoid.models import ParanoidModel
from institutions.models import Institution
from users.models import User


class Voucher(ParanoidModel):
    # Relationships
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    #  Fields
    name = models.TextField()
    code = models.TextField()
    max_uses = models.IntegerField(default=0)
    uses = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["code"], name="unique voucher code")
        ]

    def __str__(self):
        return str(self.pk)
