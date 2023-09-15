"""supply_intelligence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

import assignments

urlpatterns = [
    path("v1/assignments/", include("assignments.urls")),
    path("v1/studentassignments/", include("studentassignments.urls")),
    path("v1/comments/", include("comments.urls")),
    path("v1/documents/", include("documents.urls")),
    path("v1/institutions/", include("institutions.urls")),
    path("v1/references/", include("references.urls")),
    path("v1/users/", include("users.urls")),
    path("v1/sessions/", include("sessions.urls")),
    path("v1/tracks/", include("tracks.urls")),
    path("v1/vouchers/", include("vouchers.urls")),
    path("v1/clazzes/", include("clazzes.urls")),
    path("v1/events/", include("events.urls")),
    path("v1/merits/", include("merits.urls")),
    # DRF JWT
    path(
        "v1/auth/signin/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "v1/auth/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
] + static("/public/", document_root=settings.MEDIA_ROOT)
