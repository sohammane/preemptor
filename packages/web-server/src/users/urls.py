from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("", api.UserExperienceViewSet)
urlpatterns = [
    path("", views.UserView.as_view(), name="user"),
    path("experiences/", include(router.urls)),
    path("<pk>/institution/", views.add_institution, name="user_add_instution",),
    path("<pk>/group/", views.update_group, name="update_group",),
    path("<pk>/", views.UserView.as_view(), name="user_specifics"),
]
