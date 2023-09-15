from rest_framework import serializers
from . import models

from clazzes.serializers import ClazzSerializer


class StudentAssignmentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.clazz:
            response["clazz"] = ClazzSerializer(
                instance.clazz, context=self.context
            ).data
        return response

    class Meta:
        ordering = ["-id"]
        model = models.StudentAssignment
        fields = [
            "id",
            "assignment",
            "user",
            "clazz",
            "status",
            "grade",
            "final_comment",
            "created_at",
            "updated_at",
        ]
