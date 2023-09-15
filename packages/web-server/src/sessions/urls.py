from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register("", api.SessionViewSet)
urlpatterns = [path("last/", api.end_session, name="end_session"),] + router.urls
