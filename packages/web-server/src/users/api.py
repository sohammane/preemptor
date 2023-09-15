from rest_framework import viewsets, permissions

from . import serializers
from . import models


class UserExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Track class"""

    queryset = models.UserExperience.objects.all()
    serializer_class = serializers.UserExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        base_queryset = models.UserExperience.objects.all()
        if not self.request.user.is_superuser:
            base_queryset = base_queryset.filter(user=self.request.user)
        return base_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
