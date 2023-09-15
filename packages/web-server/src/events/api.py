from rest_framework import viewsets, permissions

from . import serializers
from . import models


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for the Voucher class"""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = []

    def get_queryset(self):
        base_queryset = self.queryset.filter(
            user__institution=self.request.user.institution
        )
        if self.request.GET.get("user__full_name"):
            base_queryset = base_queryset.filter(
                user__first_name__icontains=self.request.GET.get("user__full_name")
            ) | base_queryset.filter(
                user__last_name__icontains=self.request.GET.get("user__full_name")
            )
        if self.request.GET.get("status"):
            base_queryset = base_queryset.filter(status=self.request.GET.get("status"))
        if self.request.GET.get("created_at__gte"):
            base_queryset = base_queryset.filter(
                created_at__gte=self.request.GET.get("created_at__gte")
            )
        if self.request.GET.get("created_at__lte"):
            base_queryset = base_queryset.filter(
                created_at__lte=self.request.GET.get("created_at__lte")
            )
        return base_queryset
