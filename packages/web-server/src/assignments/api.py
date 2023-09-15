from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import Http404

from . import serializers
from . import models
from notifications.services import mail

from users.models import User
from studentassignments.models import StudentAssignment
from documents.models import Document


class AssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Assignment class"""

    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        base_queryset = self.get_queryset()
        if not self.request.user.is_superuser:
            # student can only see assignments which were assigned to
            if self.request.user.role == User.ROLE_STUDENT:
                base_queryset = base_queryset.filter(
                    studentassignment__in=StudentAssignment.objects.filter(
                        user=self.request.user
                    )
                ).exclude(status=models.Assignment.ASSIGNMENT_DRAFT)
            # supervisor can see every assignment on his institution
            elif self.request.user.role == User.ROLE_SUPERVISOR:
                base_queryset = base_queryset.filter(
                    user__institution=self.request.user.institution
                )
            else:
                base_queryset = base_queryset.filter(user=self.request.user)

        queryset = self.filter_queryset(base_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # prepare these data for the case this assignment is being created by a student
        document_id = None
        if "document" in data:
            document_id = data["document"]
            del data["document"]

        # only professor can create assignments
        if request.user.role == User.ROLE_PROFESSOR:
            data["user"] = request.user.id
        # student can do it too via documents
        elif request.user.role == User.ROLE_STUDENT and "advisor_email" in data:
            try:
                data["user"] = User.objects.get(email=data["advisor_email"]).id
            except User.DoesNotExist:
                raise Http404

            data["status"] = models.Assignment.ASSIGNMENT_OPEN

            # check if this is being sent duplicate
            if document_id:
                try:
                    document = Document.objects.get(pk=document_id)
                    if document.assignment:
                        raise "Duplicate!"
                except Exception as e:
                    print(e)
                    return Response(
                        {"detail": "An assignment for this document already exists."},
                        status=status.HTTP_409_CONFLICT,
                    )
        else:
            return Response(
                {"detail": "advisor_email is required if user is not professor."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        assignment = serializer.save()

        if request.user.role == User.ROLE_STUDENT:
            # create an studentassignment for this student
            studentAssignment = StudentAssignment(
                user=request.user, assignment=assignment
            )
            studentAssignment.save()

            # associate document and assignments
            document = Document.objects.get(id=document_id)
            document.assignment = assignment
            document.studentassignment = studentAssignment
            document.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        assignment = serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # make all studentassignments go to review
        if request.data.get("status") == models.Assignment.ASSIGNMENT_CLOSED:
            studentassignments = StudentAssignment.objects.filter(assignment=assignment)
            for studentassignment in studentassignments:
                studentassignment.status = StudentAssignment.ASSIGNMENT_IN_REVISION
                studentassignment.save()

        if (
            request.data.get("final_comment")
            and request.data.get("final_comment") != ""
        ):
            try:
                # notify students that the professor commented on the assignment
                professor = assignment.user
                studentassignments = StudentAssignment.objects.filter(
                    assignment=assignment
                ).select_related("user")
                for studentassignment in studentassignments:
                    student = studentassignment.user
                    mail(
                        student.first_name,
                        student.email,
                        params={
                            "title": "A Professor Commented On An Assignment",
                            "body": professor.first_name
                            + " commented on an assignment. Click the button below to check it out.",
                            "cta_text": "Open Assignment",
                            "cta_url": "https://app.preemptor.ai/assignment/{}".format(
                                assignment.id
                            ),
                        },
                    )
            except Exception as e:
                print(e)

        return Response(serializer.data)
