from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("", api.DocumentViewSet)
urlpatterns = [
    path("<pk>/similar/", views.similar_documents, name="similar_documents"),
] + router.urls
