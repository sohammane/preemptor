from rest_framework import serializers
from . import models
from documents.models import Document


class MeritSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            response["document"] = {
                "id": instance.document.id,
                "name": instance.document.name,
            }
        except:
            pass
        return response

    class Meta:
        ordering = ["-id"]
        model = models.Merit
        fields = [
            "id",
            "user",
            "merit_type",
            "quantity",
            "document",
            "created_at",
            "updated_at",
        ]
