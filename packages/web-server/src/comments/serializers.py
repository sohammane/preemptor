from rest_framework import serializers
from . import models
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        ordering = ["id"]
        model = models.Comment
        fields = [
            "id",
            "document",
            "user",
            "data",
            "created_at",
            "updated_at",
        ]
