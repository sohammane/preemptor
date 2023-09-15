from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from . import models

from users.models import User


class InstitutionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Institution class"""

    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["put"], detail=True, permission_classes=[permissions.IsAuthenticated])
    def user(self, request, pk=None):
        try:
            users_id = [int(x) for x in request.POST.get("users_id").split(",")]
        except ValueError:
            return Response(
                {"detail": "Invalid users_id format"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except AttributeError:
            return Response({"datail": "users_id should exist"}, status=status.HTTP_400_BAD_REQUEST)

        institution = self.get_object()
        for user_id in users_id:
            user = User.objects.get(id=user_id)
            institution.users.add(user)

        return Response({"detail": "Added successfully"})

    @user.mapping.delete
    def remove(self, request, pk=None):
        try:
            users_id = [int(x) for x in request.POST.get("users_id").split(",")]
        except ValueError:
            return Response(
                {"detail": "Invalid users_id format"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except AttributeError:
            return Response({"datail": "users_id should exist"}, status=status.HTTP_400_BAD_REQUEST)

        institution = self.get_object()
        for user_id in users_id:
            user = User.objects.get(id=user_id)
            institution.users.remove(user)

        return Response({"detail": "Removed successfully"})
