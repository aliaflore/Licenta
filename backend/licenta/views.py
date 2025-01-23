from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
import itertools
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotAuthenticated
from licenta.models import AnalysisCategory, AnalysisProvider, User, AnalysisPDF, Analysis, RadiographyPDF, AnalysisResult, PatientInvite
from licenta.serializers import (
    DoctorInviteSerializer,
    FullAnalysisCategorySerializer,
    FullAnalysisProviderSerializer,
    HistorySerializer,
    ListAnalysisSerializer,
    PatientInviteSerializer,
    UserSerializer,
    AnalysisPDFSerializer,
    AnalysisSerializer,
    RadiographyPDFSerializer,
    AnalysisResultsSerializer,
)
from .tasks import add_suggestion, notify_patient_about_invite, extract_data_from_pdf, import_all_analysis_categories
import logging


logger = logging.getLogger(__name__)


class PermissionIsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor or request.user.is_superuser


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, PermissionIsDoctor]

    @action(detail=False)
    def me(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user, context={"request": request})
            return Response(data={"user": serializer.data})
        return Response({"error": "not logged in"})


class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_doctor=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnalysisPDFViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AnalysisPDF.objects.select_related('analysis').all()
    serializer_class = AnalysisPDFSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['pk', 'created', 'taken_on']

    def get_queryset(self):
        request: Request = self.request # type: ignore
        queryset = super().get_queryset().filter(user=self.request.user)
        if request.query_params.get("user"):
            if (
                request.user.is_superuser or (
                    request.user.is_doctor and PatientInvite.objects.filter(
                        accepted=True,
                        doctor=request.user,
                        patient_id=request.query_params["user"]
                    ).exists()
                )
            ):
                queryset= super().get_queryset().filter(user_id=request.query_params["user"])
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RadiographyPDFViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RadiographyPDF.objects.all()
    serializer_class = RadiographyPDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request: Request = self.request # type: ignore
        queryset = super().get_queryset().filter(user=self.request.user)
        if request.query_params.get("user"):
            if (
                request.user.is_superuser or (
                    request.user.is_doctor and PatientInvite.objects.filter(
                        accepted=True,
                        doctor=request.user,
                        patient_id=request.query_params["user"]
                    ).exists()
                )
            ):
                queryset= super().get_queryset().filter(user_id=request.query_params["user"])
        return queryset


class AnalysisViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self): # type: ignore
        if self.action == "list":
            return ListAnalysisSerializer
        return AnalysisSerializer

    def get_queryset(self):
        request: Request = self.request # type: ignore
        queryset = super().get_queryset().filter(source__user=self.request.user)
        if request.query_params.get("user"):
            if (
                request.user.is_superuser or (
                    request.user.is_doctor and PatientInvite.objects.filter(
                        accepted=True,
                        doctor=request.user,
                        patient_id=request.query_params["user"]
                    ).exists()
                )
            ):
                queryset= super().get_queryset().filter(source__user_id=request.query_params["user"])
        return queryset


class AnalysisResultsViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request: Request = self.request # type: ignore
        queryset = super().get_queryset().filter(analysis__source__user=self.request.user)
        if request.query_params.get("user"):
            if (
                request.user.is_superuser or (
                    request.user.is_doctor and PatientInvite.objects.filter(
                        accepted=True,
                        doctor=request.user,
                        patient_id=request.query_params["user"]
                    ).exists()
                )
            ):
                queryset= super().get_queryset().filter(analysis__source__user_id=request.query_params["user"])
        if request.query_params.get("category"):
            queryset = queryset.filter(category_id=request.query_params["category"])
        names = request.query_params.getlist("name")
        if names:
            data = queryset.all()
            return filter(lambda x: x.name in names, data)
        return queryset

    @action(detail=True, methods=["post"])
    def regenerate_suggestions(self, request):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated
        object = self.get_object()
        add_suggestion.delay(object.pk)
        return Response({"status": "The suggestion is being generated."})


class AnalysisCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AnalysisCategory.objects.prefetch_related("related_names").all()
    serializer_class = FullAnalysisCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class HistoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AnalysisResult.objects.order_by("category", "name", "analysis__date")\
        .select_related("category", "analysis").all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        request: Request = self.request # type: ignore
        queryset = super().get_queryset().filter(analysis__source__user=self.request.user)
        if request.query_params.get("user"):
            if (
                request.user.is_superuser or (
                    request.user.is_doctor and PatientInvite.objects.filter(
                        accepted=True,
                        doctor=request.user,
                        patient_id=request.query_params["user"]
                    ).exists()
                )
            ):
                queryset= super().get_queryset().filter(analysis__source__user_id=request.query_params["user"])
        analyses = request.query_params.getlist("analysis")
        if analyses:
            analyses_tuples = set(map(lambda x: tuple(x.split(":")), analyses))
            return filter(lambda x: (x.category.name, x.name) in analyses_tuples, queryset.all())
        return queryset


class AnalysisProviderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AnalysisProvider.objects.all()
    serializer_class = FullAnalysisProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class PatientInvitesViewSet(viewsets.ModelViewSet):
    queryset = PatientInvite.objects.all()
    serializer_class = PatientInviteSerializer
    permission_classes = [permissions.IsAuthenticated, PermissionIsDoctor]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__email', 'patient__username']

    def get_queryset(self):
        request: Request = self.request # type: ignore
        if request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(doctor=request.user)

    @action(detail=True, methods=["post"])
    def resend(self, request, pk=None):
        invite = self.get_object()
        if invite.accepted:
            return Response({"error": "The invite has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)
        notify_patient_about_invite.delay(invite.pk)
        return Response({"status": "The invite has been resent."})


class DoctorInvitesViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = PatientInvite.objects.all()
    serializer_class = DoctorInviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request: Request = self.request # type: ignore
        if request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(patient=request.user)
