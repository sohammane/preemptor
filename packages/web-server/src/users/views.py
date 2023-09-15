from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from django.db.models import BooleanField, Case, When, Value
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.core.paginator import Paginator
from django.http import Http404
from _main import utils
from . import serializers
from .models import User
from merits.models import Merit
from vouchers.models import Voucher
from notifications import services as NotificationService
from studentassignments.models import StudentAssignment


def check_profile_completion(user):
    # add metrits for filling up the profile
    if (
        user.avatar
        and user.first_name
        and user.last_name
        and user.mobile
        and user.about
        and user.skills
    ):
        try:
            Merit.objects.filter(user=user, merit_type=Merit.TYPE_PROFILE_COMPLETE)[0]
            return None
        except:
            # create a merit if it doesn't exist
            merit = Merit(
                user=user,
                merit_type=Merit.TYPE_PROFILE_COMPLETE,
                quantity=Merit.QUANTITIES[Merit.TYPE_PROFILE_COMPLETE],
            )
            merit.save()
            return Merit.QUANTITIES[Merit.TYPE_PROFILE_COMPLETE]


class UserView(APIView, api_settings.DEFAULT_PAGINATION_CLASS):
    permission_classes = ()
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        except ValueError:
            raise ParseError

    def get(self, request, pk=None):
        if pk is not None:
            if pk == "me":
                if request.user.is_authenticated:
                    queryset = self.get_object(request.user.id)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                queryset = self.get_object(pk)
            serializer = serializers.UserSerializer(
                queryset, context={"request": request}
            )
            return Response(serializer.data)
        else:
            queryset = User.objects.all()

            if request.GET.get("query"):
                queryset = (
                    queryset.filter(first_name__icontains=request.GET.get("query"))
                    | queryset.filter(last_name__icontains=request.GET.get("query"))
                    | queryset.filter(email__icontains=request.GET.get("query"))
                )
            if request.GET.get("institution"):
                queryset = queryset.filter(institution=request.GET.get("institution"))
            if request.GET.get("only_my_institution"):
                queryset = queryset.filter(institution=request.user.institution)
            if request.GET.get("only_students"):
                queryset = queryset.filter(role=User.ROLE_STUDENT)
            if request.GET.get("assignment"):
                if request.GET.get("exclude_assigned_users"):
                    queryset = queryset.exclude(
                        studentassignment__in=StudentAssignment.objects.filter(
                            assignment=request.GET.get("assignment")
                        )
                    )
                else:
                    queryset = queryset.filter(
                        studentassignment__in=StudentAssignment.objects.filter(
                            assignment=request.GET.get("assignment")
                        )
                    )

            results = self.paginate_queryset(queryset, request, view=self)
            serializer = serializers.UserSerializer(
                results, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        voucher = None
        if "voucher" in data:
            try:
                voucher = Voucher.objects.get(code=data["voucher"])
                if voucher.max_uses > 0 and voucher.uses >= voucher.max_uses:
                    raise "Max uses reached!"
            except:
                return Response(
                    {"voucher": "Invalid voucher"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        if (
            "role" in data
            and data["role"] == User.ROLE_ADMIN
            and (not request.user or not request.user.is_superuser)
        ):
            data["role"] = User.ROLE_STUDENT

        serializer = serializers.UserSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if voucher:
            user.institution = voucher.institution
            user.save()
            voucher.uses += 1
            voucher.save()

        # add registering metrics
        merit = Merit(
            user=user,
            merit_type=Merit.TYPE_REGISTER,
            quantity=Merit.QUANTITIES[Merit.TYPE_REGISTER],
        )
        merit.save()
        # add profile metrics
        check_profile_completion(user)

        return Response(serializer.data)

    def put(self, request, pk):
        if pk == "me":
            if request.user.is_authenticated:
                queryset = self.get_object(request.user.id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            queryset = self.get_object(pk)

        # don't allow update voucher
        data = request.data
        if "voucher" in data and len(data["voucher"]) > 0:
            data["voucher"] = None
        if (
            "role" in data
            and data["role"] == User.ROLE_ADMIN
            and (not request.user or not request.user.is_superuser)
        ):
            data["role"] = User.ROLE_STUDENT

        serializer = serializers.UserSerializer(
            queryset, data=data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.save()

            if pk == "me" or pk == request.user.id:
                check_profile_completion(user)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if pk == "me":
            if request.user.is_authenticated:
                queryset = self.get_object(request.user.id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            queryset = self.get_object(pk)

        # don't allow update voucher
        data = request.data
        if "voucher" in data and len(data["voucher"]) > 0:
            data["voucher"] = None

        if (
            "role" in data
            and data["role"] == User.ROLE_ADMIN
            and (not request.user or not request.user.is_superuser)
        ):
            data["role"] = User.ROLE_STUDENT

        serializer = serializers.UserSerializer(
            queryset, data=data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # add metrits for filling up the profile
        if pk == "me" or str(pk) == str(request.user.id):
            check_profile_completion(user)

        return Response(serializer.data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@login_required
def add_institution(request, pk):
    user = User.objects.get(pk=pk)
    user.institution = request.data["institution"]
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data)


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@user_passes_test(lambda u: u.is_superuser)
def update_group(request, pk):
    # group definitions
    groups = {
        "assgnments.admin": [
            "assignments.add_assignment",
            "assignments.change_assignment",
            "assignments.delete_assignment",
            "assignments.view_assignment",
        ],
        "assgnments.viewer": ["assignments.view_assignment",],
        "documents.admin": [
            "documents.add_document",
            "documents.change_document",
            "documents.delete_document",
            "documents.view_document",
        ],
        "documents.viewer": ["documents.view_document",],
        "sessions.viewer": ["sessions.view_session"],
        "tracks.viewer": ["tracks.view_track"],
    }

    # validate group name
    group_name = request.data["name"]
    if group_name not in groups:
        return Response(
            "Invalid group name: " + group_name, status=status.HTTP_400_BAD_REQUEST
        )

    # get or create the new group
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        group.permissions.set(group[group_name])

    # set user group
    user = User.objects.get(pk=pk)
    user.groups.add(group)
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data)
