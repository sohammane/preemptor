import json
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import models


class ReferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Reference class"""

    queryset = models.Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get("query", "") != "":
            qs = (
                models.Reference.objects.filter(
                    name__icontains=self.request.GET.get("query")
                )
                | models.Reference.objects.filter(
                    authors__icontains=self.request.GET.get("query")
                )
                | models.Reference.objects.filter(
                    year__icontains=self.request.GET.get("query")
                )
                | models.Reference.objects.filter(
                    journal__icontains=self.request.GET.get("query")
                )
            )
            return qs
        return models.Reference.objects.all()

    @action(detail=True, methods=["post"], name="Add reference-document relationship")
    def document(self, request, pk):
        reference = self.get_object()
        reference.documents.add(request.data["document"])
        serializer = self.get_serializer(reference)
        return Response(serializer.data)
