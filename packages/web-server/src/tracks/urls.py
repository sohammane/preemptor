from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("", api.TrackViewSet)
urlpatterns = [
    path("faces/", views.delete_faces, name="delete_faces"),
    path("register_face/", views.register_face, name="register_face"),
    path("log_face/", views.log_face, name="log_face"),
    path("voices/", views.delete_voices, name="delete_voices"),
    path("register_voice/", views.register_voice, name="register_voice"),
    path("log_voice/", views.log_voice, name="log_voice"),
    path("log_typing/", views.log_typing, name="log_typing"),
    path("log_screen/", views.log_screen, name="log_screen"),
] + router.urls
