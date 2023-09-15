from rest_framework import serializers
from . import models
from users.serializers import UserSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user, context=self.context).data
        return response

    class Meta:
        ordering = ["-id"]
        model = models.Assignment
        fields = [
            "id",
            "user",
            "name",
            "description",
            "status",
            "final_comment",
            "due_at",
            "created_at",
            "updated_at",
        ]
