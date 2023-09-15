from rest_framework import viewsets, permissions

from . import serializers
from . import models


class TrackViewSet(viewsets.ModelViewSet):
    """ViewSet for the Track class"""

    queryset = models.Track.objects.all()
    serializer_class = serializers.TrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get("session", "") != "":
            return models.Track.objects.filter(session=self.request.GET.get("session"))
        elif self.request.user.is_superuser:
            return models.Track.objects.all()
        return models.Track.objects.all()
