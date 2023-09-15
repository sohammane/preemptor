from rest_framework import serializers
from . import models

from users.serializers import UserSerializer


class SessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        ordering = ["-id"]
        model = models.Session
        fields = [
            "id",
            "user",
            "document",
            "is_authenticated",
            "quality",
            "confidence",
            "created_at",
            "updated_at",
            "ended_at",
        ]
