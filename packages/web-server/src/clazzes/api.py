from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Q

from users.models import User
from . import serializers
from . import models


class ClazzViewSet(viewsets.ModelViewSet):
    """ViewSet for the Clazz class"""

    queryset = models.Clazz.objects.all()
    serializer_class = serializers.ClazzSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset
        qs = (
            qs.filter(owners__in=[self.request.user])
            | qs.filter(users__in=[self.request.user])
        ).distinct()
        if self.request.GET.get("archived"):
            qs = qs.filter(archived=True)
        else:
            qs = qs.filter(archived=False)
        if self.request.GET.get("query"):
            qs = qs.filter(name__icontains=self.request.GET.get("query")) | qs.filter(
                code__icontains=self.request.GET.get("query")
            )
        if self.request.GET.get("assignment"):
            if self.request.GET.get("only_assigned"):
                qs = qs.filter(
                    studentassignment__assignment__pk__in=[
                        self.request.GET.get("assignment")
                    ]
                )
            qs = qs.annotate(
                users_in_assignment=Count(
                    "users",
                    filter=Q(
                        studentassignment__assignment__pk__in=[
                            self.request.GET.get("assignment")
                        ]
                    ),
                    distinct=True,
                )
            )
        return qs

    def create(self, request, *args, **kwargs):
        if self.request.user.role == User.ROLE_STUDENT:
            return Response(
                "User cannot create a Clazz", status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            owners=[self.request.user], institution=self.request.user.institution,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_destroy(self, instance):
        instance.archived = True
        instance.save()
