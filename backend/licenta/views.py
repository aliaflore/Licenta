from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
import itertools
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from licenta.models import AnalysisProvider, User, AnalysisPDF, Analysis, RadiographyPDF, AnalysisResult
from licenta.serializers import (
    FullAnalysisCategorySerializer,
    FullAnalysisProviderSerializer,
    ListAnalysisSerializer,
    UserSerializer,
    AnalysisPDFSerializer,
    AnalysisSerializer,
    RadiographyPDFSerializer,
    AnalysisResultsSerializer,
)
from .tasks import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def me(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user, context={"request": request})
            return Response(data={"user": serializer.data})
        return Response({"error": "not logged in"})


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
        return super().get_queryset().filter(user=self.request.user)

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
        return super().get_queryset().filter(user=self.request.user)


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
        return super().get_queryset().filter(source__user=self.request.user)


class AnalysisResultsViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(analysis__source__user=self.request.user)

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


class HistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated

        toate = (
            AnalysisResult.objects.filter(analysis__source__user=self.request.user)
            .prefetch_related("analysis")
            .all()
        )

        an_iterator = itertools.groupby(
            sorted(list(toate), key=lambda x: x.name), lambda x: x.name
        )
        results = []

        for key, group in an_iterator:
            d = {
                "name": str(key), 
                "category": next(group).category.name,
                "data": []
            }
            for analiza in group:
                d["data"].append(
                    {
                        "date": analiza.analysis.date,
                        "in_range": analiza.in_range,
                        "result": analiza.result,
                        "range_min": analiza.range_min,
                        "range_max": analiza.range_max,
                        "refference_range": analiza.refference_range,
                        "measurement_unit": analiza.measurement_unit,
                        "suggestion": analiza.suggestion,
                    }
                )
            results.append(d)

        return Response({"results": results})


class AnalysisProviderViewSet(viewsets.ModelViewSet):
    queryset = AnalysisProvider.objects.all()
    serializer_class = FullAnalysisProviderSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = None