from django.urls import path, include
from rest_framework import routers

from . import api


router = routers.DefaultRouter()
router.register("", api.CommentViewSet)
urlpatterns = router.urls
