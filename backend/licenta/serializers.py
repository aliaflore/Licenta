from rest_framework import serializers

from licenta.models import User, RadiographyPDF, AnalysisPDF, AnalysisResult, Analysis


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "url", "username", "email", "is_staff")
        read_only_fields = ["is_staff"]


class RadiographyPDFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadiographyPDF
        fields = ("id", "url", "file", "source", "user", "created")


class AnalysisPDFSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnalysisPDF
        fields = ("url", "file", "source", "user", "created")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AnalysisResultsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = (
            "url",
            "name",
            "is_numeric",
            "result",
            "range_min",
            "range_max",
            "expected",
            "measurement_unit",
            "analysis",
            "suggestion"
        )



class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    results = AnalysisResultsSerializer(read_only=True, many=True)

    class Meta:
        model = Analysis
        fields = ("url", "user", "source", "created", "results")
