from rest_framework import serializers
from . import models

from users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)

        if instance.user:
            response["user"] = UserSerializer(instance.user, context=self.context).data

        return response

    class Meta:
        ordering = ordering = ["status", "-id"]
        model = models.Event
        fields = [
            "id",
            "user",
            "document",
            "event_type",
            "status",
            "confidence",
            "quality",
            "created_at",
            "updated_at",
        ]
