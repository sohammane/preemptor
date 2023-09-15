from rest_framework import serializers
from . import models


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ["-id"]
        model = models.Institution
        fields = [
            "id",
            "name",
            "msg_auth_good_1",
            "msg_auth_bad_1",
            "msg_auth_bad_2",
            "msg_auth_bad_3",
            "msg_auth_good_after_bad",
            "msg_copy_paste",
            "msg_1000_merits",
            "has_typing_cadence",
            "has_facial_recognition",
            "has_voice_recognition",
            "has_screen_invigilation",
            "created_at",
            "updated_at",
        ]
