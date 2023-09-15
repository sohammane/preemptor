from rest_framework import serializers
from . import models
from users.serializers import UserSerializer


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ["-id"]
        model = models.Reference
        fields = [
            "id",
            "documents",
            "name",
            "year",
            "authors",
            "journal",
            "url",
            "location",
            "created_at",
            "updated_at",
        ]
