from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("", api.EventViewSet)
urlpatterns = [
    path("meta/", views.get_meta, name="events_meta"),
    path("notify/", views.notify, name="events_notify"),
] + router.urls
