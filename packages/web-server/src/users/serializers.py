from rest_framework import serializers
from django.db.models import Sum

from _main.utils import FieldMixin
from merits.models import Merit
from institutions.serializers import InstitutionSerializer
from . import models
from . import utils


class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ["-id"]
        model = models.UserExperience
        fields = [
            "id",
            "user",
            "type",
            "name",
            "subname",
            "description",
            "date_start",
            "date_end",
            "created_at",
            "updated_at",
        ]


class UserSerializer(FieldMixin, serializers.ModelSerializer):
    experiences = UserExperienceSerializer(
        source="userexperience_set", many=True, read_only=True
    )
    merits = serializers.IntegerField(read_only=True)
    originality_score = serializers.FloatField(read_only=True)
    password = serializers.CharField(write_only=True)
    has_typing = serializers.BooleanField(read_only=True)
    has_face = serializers.BooleanField(read_only=True)
    has_voice = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        if "is_superuser" in validated_data and validated_data["is_superuser"]:
            user.role = models.User.ROLE_ADMIN
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
        if "is_superuser" in validated_data and validated_data["is_superuser"]:
            user.role = models.User.ROLE_ADMIN
        user.save()
        return user

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["institution"] = InstitutionSerializer(
            instance.institution, context=self.context
        ).data
        response["merits"] = Merit.objects.filter(user=instance.id).aggregate(
            total=Sum("quantity")
        )["total"]
        response["originality_score"] = utils.originality_score(instance)
        return response

    class Meta:
        ordering = ["-id"]
        model = models.User
        fields = [
            "id",
            "role",
            "is_superuser",
            "institution",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "mobile",
            "student_number",
            "academic_level",
            "other_academic_level",
            "university",
            "curriculum",
            "avatar",
            "merits",
            "cover",
            "about",
            "skills",
            "hobbies",
            "headline",
            "voucher",
            "experiences",
            "last_tdna_text",
            "originality_score",
            "has_typing",
            "has_face",
            "has_voice",
            "datetime_last_writing",
            "datetime_last_face",
            "datetime_last_voice",
            "password",
            "created_at",
            "updated_at",
        ]

