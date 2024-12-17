from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from licenta.views import (
    AnalysisCategoryViewSet,
    AnalysisProviderViewSet,
    UserViewSet,
    AnalysisPDFViewSet,
    RadiographyPDFViewSet,
    AnalysisViewSet,
    AnalysisResultsViewSet,
    HistoryViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"analysis-pdf", AnalysisPDFViewSet)
router.register(r"radiography-pdf", RadiographyPDFViewSet)
router.register(r"analysis", AnalysisViewSet)
router.register(r"analysis-providers", AnalysisProviderViewSet)
router.register(r"analysis-results", AnalysisResultsViewSet)
router.register(r"analysis-category", AnalysisCategoryViewSet)
router.register(r"history", HistoryViewSet, basename="history")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
