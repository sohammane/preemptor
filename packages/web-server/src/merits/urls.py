from django.urls import path, include
from rest_framework import routers

from . import api


router = routers.DefaultRouter()
router.register("", api.MeritViewSet)
urlpatterns = router.urls

urlpatterns = [] + router.urls

