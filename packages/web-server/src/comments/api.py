from rest_framework import viewsets, permissions

from . import serializers
from . import models


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Comment class"""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get("document"):
            return models.Comment.objects.filter(
                document=self.request.GET.get("document")
            )
        return models.Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
