from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from . import serializers
from . import models
from . import utils

from documents.models import Document


class SessionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Session class"""

    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get("document"):
            document = Document.objects.get(pk=self.request.GET.get("document"))
            return models.Session.objects.filter(document=document, user=document.user)
        elif self.request.user.is_superuser:
            return models.Session.objects.all()
        return models.Session.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # end last session before creating a new one
        last_session = utils.get_last_session(self.request.user)
        utils.end_session(last_session)

        # create a new session
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        utils.end_session(instance)


@api_view(("DELETE",))
@renderer_classes((JSONRenderer,))
@login_required
def end_session(request):
    last_session = utils.get_last_session(request.user)
    utils.end_session(last_session)
    return Response()
