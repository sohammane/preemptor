from rest_framework import serializers
from . import models


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ["-id"]
        model = models.Track
        fields = [
            "id",
            "session",
            "type",
            "blob",
            "data",
            "metadata",
            "is_authenticated",
            "quality",
            "confidence",
            "created_at",
        ]
