from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
import itertools
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from licenta.models import User, AnalizePDF, Analize, RadiografiePDF, AnalizeRezultate
from licenta.serializers import (
    UserSerializer,
    AnalizePDFSerializer,
    AnalizeSerializer,
    RadiografiePDFSerializer,
    AnalizeRezultateSerializer,
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


class AnalizePDFViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AnalizePDF.objects.all()
    serializer_class = AnalizePDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RadiografiePDFViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RadiografiePDF.objects.all()
    serializer_class = RadiografiePDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AnalizeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Analize.objects.all()
    serializer_class = AnalizeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AnalizeRezultateViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AnalizeRezultate.objects.all()
    serializer_class = AnalizeRezultateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(analysis__user=self.request.user)


class HistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated

        toate = (
            AnalizeRezultate.objects.filter(analysis__user=self.request.user)
            .select_related("analysis")
            .all()
        )

        an_iterator = itertools.groupby(
            sorted(list(toate), key=lambda x: x.name), lambda x: x.name
        )
        results = []

        for key, group in an_iterator:
            d = {"nume": str(key), "data": []}
            for analiza in group:
                d["data"].append(
                    {
                        "date": analiza.analysis.date,
                        "is_numeric": analiza.is_numeric,
                        "result": analiza.result,
                        "range_min": analiza.range_min,
                        "range_max": analiza.range_max,
                        "expected": analiza.expected,
                        "measurement_unit": analiza.measurement_unit,
                        "suggestion": analiza.suggestion,
                    }
                )
            results.append(d)

        return Response({"results": results})
