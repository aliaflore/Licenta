from rest_framework import serializers

from licenta.models import User, RadiografiePDF, AnalizePDF, AnalizeRezultate, Analize


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "url", "username", "email", "is_staff")
        read_only_fields = ["is_staff"]


class RadiografiePDFSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.ChoiceField(choices=RadiografiePDF.SOURCES)

    class Meta:
        model = RadiografiePDF
        fields = ("id", "url", "file", "source", "user", "created")


class AnalizePDFSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnalizePDF
        fields = ("url", "file", "source", "user", "created")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AnalizeRezultateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnalizeRezultate
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



class AnalizeSerializer(serializers.HyperlinkedModelSerializer):
    results = AnalizeRezultateSerializer(read_only=True, many=True)

    class Meta:
        model = Analize
        fields = ("url", "user", "source", "created", "results")
