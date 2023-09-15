from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .models import Clazz
from users.models import User
from assignments.models import Assignment
from studentassignments.utils import create_studentassignment
from documents.utils import create_document


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def enroll(request):
    if not request.POST.get("code"):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        clazz = Clazz.objects.get(
            code=request.POST.get("code"), institution=request.user.institution,
        )
    except:
        return Response(
            {"detail": "Class not found!"}, status=status.HTTP_404_NOT_FOUND
        )

    user = (
        request.POST.get("user") and User.objects.get(pk=request.POST.get("user"))
    ) or request.user
    clazz.users.add(user)
    clazz.save()

    # get this clazz's assignments
    assignments = Assignment.objects.filter(studentassignment__clazz__pk=clazz.id)
    for assignment in assignments:
        # create an studentassignment and a document for this user, for each assignment
        create_studentassignment(
            {"user": user, "assignment": assignment, "clazz": clazz.id}
        )
        create_document({"assignment": assignment}, user)

    return Response(status=status.HTTP_201_CREATED)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def unenroll(request, pk):
    try:
        clazz = Clazz.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    clazz.users.remove(request.POST.get("user") or request.user)
    clazz.save()

    return Response(status=status.HTTP_200_OK)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def assign(request, pk):
    try:
        clazz = Clazz.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    assignment = request.POST.get("assignment")

    # create an studentassignment and a document for each user in this clazz
    for user in clazz.users.all():
        create_studentassignment(
            {"user": user.id, "assignment": assignment, "clazz": clazz.id}
        )
        create_document({"assignment": assignment}, user)

    return Response(status=status.HTTP_200_OK)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def undelete(request, pk):
    try:
        clazz = Clazz.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    clazz.archived = False
    clazz.save()

    return Response(status=status.HTTP_200_OK)
