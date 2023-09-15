from rest_framework import serializers
from . import models
from users.serializers import UserSerializer

from assignments.models import Assignment
from assignments.serializers import AssignmentSerializer
from users.serializers import UserSerializer


class ClazzSerializer(serializers.ModelSerializer):
    assignments = serializers.IntegerField(read_only=True)
    users_in_assignment = serializers.IntegerField(read_only=True)
    owners = UserSerializer(
        many=True, read_only=True, context={"fields": ["full_name"]}
    )
    users = UserSerializer(many=True, read_only=True, context={"fields": ["full_name"]})

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["assignments"] = AssignmentSerializer(
            Assignment.objects.filter(
                studentassignment__clazz__pk=instance.id
            ).distinct(),
            many=True,
            context=self.context,
        ).data
        return response

    class Meta:
        ordering = ["-id"]
        model = models.Clazz
        fields = [
            "id",
            "code",
            "institution",
            "owners",
            "users",
            "name",
            "description",
            "archived",
            "assignments",
            "users_in_assignment",
            "created_at",
            "updated_at",
        ]
