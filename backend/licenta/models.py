from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AbstractPDF(models.Model):
    ARCADIA = 0
    REGINA_MARIA = 1
    SYNEVO = 2
    NONE = 100
    SOURCES = {
        ARCADIA: "Arcadia",
        REGINA_MARIA: "Regina Maria",
        SYNEVO: "Synevo",
        NONE: "None",
    }

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    source = models.IntegerField(
        choices=SOURCES,
        default=NONE,
    )

    class Meta:
        abstract = True


class AnalizePDF(AbstractPDF):
    file = models.FileField(upload_to="analize-pdfs/")


class RadiografiePDF(AbstractPDF):
    file = models.FileField(upload_to="radiografie-pdfs/")


class Analize(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    source = models.OneToOneField(
        "AnalizePDF",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True)


class AnalizeRezultate(models.Model):
    name = models.CharField(max_length=255)
    is_numeric = models.BooleanField()
    result = models.DecimalField(max_digits=10, decimal_places=2)
    range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    expected = models.BooleanField(null=True)
    measurement_unit = models.CharField(max_length=10)
    suggestion = models.TextField(null=True)

    analysis = models.ForeignKey(
        "Analize", on_delete=models.CASCADE, related_name="results"
    )
