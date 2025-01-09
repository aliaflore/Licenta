from rest_framework import serializers

from licenta.models import AnalysisCategory, AnalysisProvider, User, RadiographyPDF, AnalysisPDF, AnalysisResult, Analysis


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "url", "username", "email", "is_staff")
        read_only_fields = ("is_staff",)


class AnalysisProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalysisProvider
        fields = ("pk", "name")
        read_only_fields = fields


class FullAnalysisProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalysisProvider
        fields = (
            "pk",
            "url",
            "name",
            "crops_words",
            "crops_pixels",
            "crop_similarity",
            "line_height_tolerance",
            "word_width_tolerance",
            "line_continuation_difference_width",
            "category_similarity",
            "range_extraction_regex",
            "ignored_words",
            "space_pixels",
            "replace_results",
            "analysis_list",
            "analysis_providedlang",
            "analysis_list_skip_first_row",
            "analysis_list_skip_first_table",
            "analysis_columns",
        )


class RadiographyPDFSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    provider = AnalysisProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=AnalysisProvider.objects.all(),
        required=True,
        write_only=True,
        source="provider",
    )

    class Meta:
        model = RadiographyPDF
        fields = ("pk", "url", "file", "provider", "user", "created", "taken_on", "doctor_notes", "provider_id", "created", "modified")
        read_only_fields = ("created", "url")
        required_fields = ("file", "provider_id")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AnalysisPDFSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    provider = AnalysisProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=AnalysisProvider.objects.all(),
        required=True,
        write_only=True,
        source="provider",
    )

    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis-detail",
        required=False,
        allow_null=True,
        read_only=True,
    )

    analysis_id = serializers.PrimaryKeyRelatedField(
        required=False,
        source="analysis",
        read_only=True,
    )

    class Meta:
        model = AnalysisPDF
        fields = (
            "pk", "url", "file", "provider", "user", "created", "taken_on", "doctor_notes", "suggestion", "provider_id",
            "analysis", "analysis_id", "created", "modified")
        read_only_fields = ("created", "url")
        extra_kwargs = {
            'file': {'required': True},
        }

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AnalysisCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalysisCategory
        fields = ("pk", "name")
        read_only_fields = fields


class FullAnalysisCategorySerializer(serializers.HyperlinkedModelSerializer):
    related_names = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = AnalysisCategory
        fields = ("pk", "name", "related_names")
        read_only_fields = fields


class AnalysisResultsAnalysisRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Analysis.objects.filter(source__user=self.context["request"].user)


class AnalysisResultsSerializer(serializers.HyperlinkedModelSerializer):
    category = FullAnalysisCategorySerializer(read_only=True)
    analysis_id = AnalysisResultsAnalysisRelatedField(
        required=True,
        write_only=True,
        source="analysis",
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=AnalysisCategory.objects.all(),
        required=True,
        write_only=True,
        source="category",
    )

    class Meta:
        model = AnalysisResult
        fields = (
            "url",
            "pk",
            "name",
            "category",
            "result",
            "measurement_unit",
            "refference_range",
            "range_min",
            "range_max",
            "in_range",
            "suggestion",
            "doctor_note",
            "category_id",
            "analysis_id",
            "created",
            "modified"
        )
        read_only_fields = ("created", "modified", "url", "pk")


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    results = AnalysisResultsSerializer(read_only=True, many=True)
    source = AnalysisPDFSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = ("url", "source", "created", "results", "notes")
        read_only_fields = ("results", "url", "source", "created")
