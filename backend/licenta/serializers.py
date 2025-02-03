import itertools
import logging
import dj_rest_auth.serializers
from rest_framework import serializers

from licenta.models import (
    AnalysisCategory,
    AnalysisProvider,
    User,
    RadiographyPDF,
    AnalysisPDF,
    AnalysisResult,
    Analysis,
    PatientInvite,
)

from django.utils import timezone 
from datetime import timedelta

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.utils import build_absolute_uri
from allauth.account.utils import user_pk_to_url_str

logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.SerializerMethodField()
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    is_paying = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "url",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_doctor",
            "is_superuser",
            "full_name",
            "date_joined",
            "password1",
            "password2",
            "is_paying",
            "accept_new_patients",
            "birth_date",
            "phone_number",
            "height",
            "weight",
        )
        read_only_fields = tuple(filter(lambda x: x not in (
            "first_name", "last_name", "accept_new_patients", "birth_date", "phone_number", "height", "weight"
        ), fields))

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def validate(self, attrs):
        if ("password1" in attrs and "password2" not in attrs):
            raise serializers.ValidationError(
                {"password2": "This field is required"}
            )
        if ("password1" not in attrs and "password2" in attrs):
            raise serializers.ValidationError(
                {"password1": "This field is required"}
            )
        if "password1" in attrs and "password2" in attrs:
            if attrs["password1"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password2": "Passwords do not match"}
                )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        user: User = super().update(instance, validated_data)
        if "password1" in validated_data:
            logger.info("Setting password for user %s: %s", user, validated_data["password1"])
            user.set_password(validated_data["password1"])
            user.save()
        return user


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
        fields = (
            "pk",
            "url",
            "file",
            "provider",
            "user",
            "created",
            "taken_on",
            "doctor_notes",
            "provider_id",
            "created",
            "modified",
        )
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
            "pk",
            "url",
            "file",
            "provider",
            "user",
            "created",
            "taken_on",
            "doctor_notes",
            "suggestion",
            "provider_id",
            "analysis",
            "analysis_id",
            "created",
            "modified",
        )
        read_only_fields = ("created", "url")
        extra_kwargs = {
            "file": {"required": True},
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
            "approve_ai_suggestion",
            "doctor_note",
            "category_id",
            "analysis_id",
            "created",
            "modified",
        )
        read_only_fields = ("created", "modified", "url", "pk")


class SimpleAnalysisResultsSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.DateField(source="analysis.date", read_only=True)
    analysis_id = serializers.PrimaryKeyRelatedField(
        required=False,
        source="analysis",
        read_only=True,
    )

    class Meta:
        model = AnalysisResult
        fields = (
            "url",
            "pk",
            "date",
            "analysis_id",
            "result",
            "measurement_unit",
            "refference_range",
            "range_min",
            "range_max",
            "in_range",
            "suggestion",
            "approve_ai_suggestion",
            "doctor_note",
            "created",
            "modified",
        )
        read_only_fields = ("created", "modified", "url", "pk")


class HistoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = sorted(data, key=lambda x: (x.category.id, x.name, x.analysis.date or timezone.now().date()))
        an_iterator = itertools.groupby(data, lambda x: (x.category, x.name))
        results = []

        for key, group in an_iterator:
            group = list(group)
            d = {
                "name": group[0].name,
                "category": AnalysisCategorySerializer(
                    group[0].category, context=self.context
                ).data,
                "data": [],
            }
            for analiza in group:
                try:
                    d["data"].append(
                        SimpleAnalysisResultsSerializer(
                            analiza, context=self.context
                        ).data
                    )
                except AttributeError:
                    pass
            results.append(d)
        return results


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    results = SimpleAnalysisResultsSerializer(read_only=True, many=True)

    class Meta:
        model = Analysis
        fields = ("url", "created", "results", "notes")
        read_only_fields = ("results", "url", "created")
        list_serializer_class = HistoryListSerializer


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    results = AnalysisResultsSerializer(read_only=True, many=True)
    source = AnalysisPDFSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = ("url", "source", "created", "results", "notes")
        read_only_fields = ("results", "url", "source", "created")


class ListAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    source = AnalysisPDFSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = ("url", "source", "created", "notes")
        read_only_fields = ("url", "source", "created")


class PatientInviteSerializer(serializers.HyperlinkedModelSerializer):
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    email = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        required=True,
        write_only=True,
        source="patient",
        slug_field="email"
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="patient-invites-detail", lookup_field="pk"
    )

    class Meta:
        model = PatientInvite
        fields = (
            "url",
            "pk",
            "patient",
            "email",
            "doctor",
            "accepted",
            "accepted_on",
            "created",
            "modified",
        )
        read_only_fields = tuple(filter(lambda x: x != "email", fields))

    def validate(self, attrs):
        if self.context["request"].user == attrs["patient"]:
            raise serializers.ValidationError(
                {"email": "You can't invite yourself to be your patient"}
            )
        if PatientInvite.objects.filter(
            patient=attrs["patient"],
            doctor=self.context["request"].user,
            accepted=False,
        ).exists():
            raise serializers.ValidationError(
                {"email": "You already invited this user to be your patient"}
            )
        if PatientInvite.objects.filter(
            patient=attrs["patient"], doctor=self.context["request"].user, accepted=True
        ).exists():
            raise serializers.ValidationError(
                {"email": "This user is already your patient"}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["doctor"] = self.context["request"].user
        return super().create(validated_data)


class DoctorInviteSerializer(serializers.HyperlinkedModelSerializer):
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="doctor-invites-detail", lookup_field="pk"
    )

    class Meta:
        model = PatientInvite
        fields = (
            "url",
            "pk",
            "patient",
            "patient_id",
            "doctor",
            "accepted",
            "accepted_on",
            "created",
            "modified",
        )
        read_only_fields = tuple(filter(lambda x: x != "accepted", fields))

    def update(self, instance, validated_data):
        instance.expires = timezone.now() + timedelta(days=30)
        return super().update(instance, validated_data)


class DoctorRegisterSerializer(RegisterSerializer):
    doctor_proof = serializers.FileField(required=True)

    def get_cleaned_data(self):
        original = super().get_cleaned_data()
        original["doctor_proof"] = self.validated_data.get("doctor_proof", "")
        return original

    def custom_signup(self, request, user: User):
        user.is_active = False
        user.is_doctor = True
        user.doctor_proof = self.cleaned_data.get("doctor_proof")
        user.save()
        return super().custom_signup(request, user)


class PasswordResetSerializer(dj_rest_auth.serializers.PasswordResetSerializer):
    @staticmethod
    def url_generator(request, user, temp_key):
        logger.info("Generating password reset URL for user %s", user)
        url = build_absolute_uri(None, f"/password-reset/{user_pk_to_url_str(user)}/{temp_key}")
        url = url.replace('%3F', '?')
        return url

    def get_email_options(self):
        opts = super().get_email_options()
        opts['url_generator'] = self.url_generator
        return opts
