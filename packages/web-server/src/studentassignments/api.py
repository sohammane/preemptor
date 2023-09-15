from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.http import Http404
from django.db.models import Avg, Q
from django.db.models.functions import Coalesce

from . import serializers
from . import models
from . import utils
from documents.utils import register_document_embeddings
from notifications.services import mail

from merits.models import Merit
from users.models import User
from documents.models import Document


class StudentAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Assignment class"""

    queryset = models.StudentAssignment.objects.all()
    serializer_class = serializers.StudentAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = utils.create_studentassignment(request.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        studentassignment = serializer.save()

        try:
            student = studentassignment.user
            assignment = studentassignment.assignment
            professor = studentassignment.assignment.user
            document = Document.objects.filter(
                studentassignment=studentassignment
            ).annotate(
                avg_confidence=Coalesce(
                    Avg(
                        "session__confidence",
                        filter=Q(
                            session__user__role=User.ROLE_STUDENT,
                            session__quality__gt=0,
                        ),
                    ),
                    0,
                )
            )[
                0
            ]

            # EMAILS TO STUDENT
            if request.data.get("status") == "O":
                mail(
                    student.first_name,
                    student.email,
                    params={
                        "title": "A Professor Requested Changes",
                        "body": "Professor "
                        + professor.first_name
                        + " requested changes on an assignment. Click the button below to check it out.",
                        "cta_text": "Open Assignment",
                        "cta_url": "https://app.preemptor.ai/assignment/{}".format(
                            assignment.id
                        ),
                    },
                )
            if request.data.get("status") == "G":
                if (
                    not assignment.due_at
                    or studentassignment.submitted_at < assignment.due_at
                ) and document.avg_confidence >= 0.7:
                    merit = Merit(
                        user=student,
                        merit_type=Merit.TYPE_ASSIGNMENT_SUBMIT,
                        quantity=Merit.QUANTITIES[Merit.TYPE_ASSIGNMENT_SUBMIT],
                        document=document,
                    )
                    merit.save()

                    if studentassignment.grade >= 75:
                        merit = Merit(
                            user=student,
                            merit_type=Merit.TYPE_ASSIGNMENT_GRADE_75,
                            quantity=Merit.QUANTITIES[Merit.TYPE_ASSIGNMENT_GRADE_75],
                            document=document,
                        )
                        merit.save()

                mail(
                    student.first_name,
                    student.email,
                    params={
                        "title": "A Professor Graded An Assignment",
                        "body": "Professor "
                        + professor.first_name
                        + " graded an assignment you submitted. Click the button below to check it out.",
                        "cta_text": "Open Assignment",
                        "cta_url": "https://app.preemptor.ai/assignment/{}".format(
                            assignment.id
                        ),
                    },
                )
            # EMAILS TO PROFESSOR
            if request.data.get("status") == "R":
                studentassignment.submitted_at = timezone.now()
                studentassignment.save()

                register_document_embeddings(document)

                mail(
                    professor.first_name,
                    professor.email,
                    params={
                        "title": "A Student Requested Your Review",
                        "body": student.first_name
                        + " requested your review on an assignment. Click the button below to check it out.",
                        "cta_text": "Open Assignment",
                        "cta_url": "https://app.preemptor.ai/assignment/{}".format(
                            assignment.id
                        ),
                    },
                )

        except Exception as e:
            print(e)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
