from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.static import serve
from django.views.decorators.clickjacking import xframe_options_exempt


from django.conf import settings
from licenta.views import (
    AnalysisCategoryViewSet,
    AnalysisProviderViewSet,
    DoctorRegisterView,
    UserViewSet,
    AnalysisPDFViewSet,
    RadiographyPDFViewSet,
    AnalysisViewSet,
    AnalysisResultsViewSet,
    HistoryViewSet,
    DoctorInvitesViewSet,
    PatientInvitesViewSet,
    account_inactive,
    payment_details,
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
router.register(r"patient-invites", PatientInvitesViewSet, basename="patient-invites")
router.register(r"doctor-invites", DoctorInvitesViewSet, basename="doctor-invites")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('payments/', include('payments.urls')),
    path('payment-details/<int:payment_id>/', payment_details),
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/dj-rest-auth/registration-doctor/", DoctorRegisterView.as_view()),
    path("api/dj-rest-auth/account-inactive/", account_inactive, name="account_inactive"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, view=xframe_options_exempt(serve), document_root=settings.MEDIA_ROOT)