from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("", api.ClazzViewSet)
urlpatterns = router.urls

urlpatterns = [
    path("enroll/", views.enroll, name="enroll"),
    path("<pk>/unenroll/", views.unenroll, name="unenroll"),
    path("<pk>/assign/", views.assign, name="assign"),
    path("<pk>/undelete/", views.undelete, name="undelete"),
] + router.urls

