from rest_framework import serializers
from . import models


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ["id"]
        model = models.Voucher
        fields = [
            "id",
            "institution",
            "name",
            "code",
            "max_uses",
            "uses",
            "created_at",
            "updated_at",
        ]
