from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Q

from users.models import User
from . import serializers
from . import models


class MeritViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Merit class"""

    queryset = models.Merit.objects.all()
    serializer_class = serializers.MeritSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        base_queryset = self.queryset.filter(user=self.request.user)

        if self.request.GET.get("created_at__gte"):
            base_queryset = base_queryset.filter(
                created_at__gte=self.request.GET.get("created_at__gte")
            )
        if self.request.GET.get("created_at__lte"):
            base_queryset = base_queryset.filter(
                created_at__lte=self.request.GET.get("created_at__lte")
            )
        return base_queryset
