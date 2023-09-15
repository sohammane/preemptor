from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Avg, Min, Q, F, Count, Max, IntegerField
from django.db.models.functions import Coalesce, Cast

from . import serializers
from . import models
from .utils import create_document, check_similarities
from studentassignments.models import StudentAssignment
from documents.models import Document
from users.models import User
from assignments.models import Assignment


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Document class"""

    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        base_queryset = self.get_queryset()

        # filter by status
        if self.request.GET.get("status"):
            base_queryset = base_queryset.filter(
                studentassignment__status=self.request.GET.get("status")
            )

        # documents listed on an assignment page
        if self.request.GET.get("assignment"):
            base_queryset = base_queryset.filter(
                assignment=self.request.GET.get("assignment")
            )
            # this directly affects the behaviour on the frontend
            # a user may have only one document per assignment, if he sees documents of others, his "create document" button doesnt show
            if self.request.user.role == User.ROLE_STUDENT:
                base_queryset = base_queryset.filter(user=self.request.user)
        # documents listed on professor's inbox
        # TODO list documents for supervisor roles
        elif self.request.GET.get("professor") and int(request.user.id) == int(
            self.request.GET.get("professor")
        ):
            base_queryset = base_queryset.filter(
                assignment__user=self.request.GET.get("professor")
            ).annotate(status=F("studentassignment__status"))
        # documents listed on documents page
        elif not self.request.user.is_superuser:
            base_queryset = base_queryset.filter(user=self.request.user).exclude(
                assignment__status=Assignment.ASSIGNMENT_DRAFT
            )

        # calculate doc scores if user is not student
        if request.user.role != User.ROLE_STUDENT:
            # get the aggregate metric of high quality sessions or 0
            base_queryset = base_queryset.annotate(
                has_typing=Max(
                    Cast("session__has_typing", output_field=IntegerField()),
                    filter=Q(session__user__role=User.ROLE_STUDENT),
                ),
                has_face=Max(
                    Cast("session__has_face", output_field=IntegerField()),
                    filter=Q(session__user__role=User.ROLE_STUDENT),
                ),
                has_voice=Max(
                    Cast("session__has_voice", output_field=IntegerField()),
                    filter=Q(session__user__role=User.ROLE_STUDENT),
                ),
                has_screen=Max(
                    Cast("session__has_screen", output_field=IntegerField()),
                    filter=Q(session__user__role=User.ROLE_STUDENT),
                ),
                sessions=Count(
                    "session", filter=Q(session__user__role=User.ROLE_STUDENT)
                ),
                confidence=Coalesce(
                    Avg(
                        "session__confidence",
                        filter=Q(
                            session__user__role=User.ROLE_STUDENT,
                            session__quality__gt=0,
                        ),
                    ),
                    0,
                ),
                avg_confidence=Coalesce(
                    Avg(
                        "session__confidence",
                        filter=Q(
                            session__user__role=User.ROLE_STUDENT,
                            session__quality__gt=0,
                        ),
                    ),
                    0,
                ),
                min_confidence=Coalesce(
                    Min(
                        "session__confidence",
                        filter=Q(
                            session__user__role=User.ROLE_STUDENT,
                            session__quality__gt=0,
                        ),
                    ),
                    0,
                ),
            )

        queryset = self.filter_queryset(base_queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = create_document(request.data.copy(), request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
