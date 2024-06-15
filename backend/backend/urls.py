from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from licenta.views import (
    UserViewSet,
    AnalizePDFViewSet,
    RadiografiePDFViewSet,
    AnalizeViewSet,
    AnalizeRezultateViewSet,
    HistoryViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"analizePdf", AnalizePDFViewSet)
router.register(r"radiografiePdf", RadiografiePDFViewSet)
router.register(r"analize", AnalizeViewSet)
router.register(r"analizeRezultate", AnalizeRezultateViewSet)
router.register(r"history", HistoryViewSet, basename="history")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
