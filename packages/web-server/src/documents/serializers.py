from rest_framework import serializers
from . import models
from . import utils
from assignments.serializers import AssignmentSerializer

from users.serializers import UserSerializer
from assignments.serializers import AssignmentSerializer
from studentassignments.serializers import StudentAssignmentSerializer


class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    has_typing = serializers.BooleanField(read_only=True)
    has_face = serializers.BooleanField(read_only=True)
    has_voice = serializers.BooleanField(read_only=True)
    has_screen = serializers.BooleanField(read_only=True)
    sessions = serializers.IntegerField(read_only=True)
    confidence = serializers.FloatField(read_only=True)
    avg_confidence = serializers.FloatField(read_only=True)
    min_confidence = serializers.FloatField(read_only=True)
    similarity_score = serializers.FloatField(read_only=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.raw_data is not None and len(instance.raw_data) > 0:
            response["similarity_score"], _ = utils.check_similarities(instance)

        response["user"] = UserSerializer(instance.user, context=self.context).data
        if instance.assignment:
            response["assignment"] = AssignmentSerializer(
                instance.assignment, context=self.context
            ).data
        if instance.studentassignment:
            response["studentassignment"] = StudentAssignmentSerializer(
                instance.studentassignment, context=self.context
            ).data

        return response

    class Meta:
        ordering = ["-id"]
        model = models.Document
        fields = [
            "id",
            "user",
            "assignment",
            "studentassignment",
            "name",
            "data",
            "raw_data",
            "has_template",
            "requires_face",
            "requires_voice",
            "requires_screen",
            "sessions",
            "has_typing",
            "has_face",
            "has_voice",
            "has_screen",
            "confidence",
            "status",
            "avg_confidence",
            "min_confidence",
            "pasted_chars",
            "similarity_score",
            "created_at",
            "updated_at",
        ]
