from django.contrib.auth.models import AbstractUser
from django.db import models


class AnalysisProvider(models.Model):
    name = models.CharField(max_length=25)
    crops_words = models.JSONField(blank=True)
    crops_pixels = models.JSONField(blank=True)
    crop_similarity = models.IntegerField()
    line_height_tolerance = models.IntegerField()
    word_width_tolerance = models.IntegerField()
    line_continuation_difference_width = models.IntegerField()
    category_similarity = models.IntegerField()
    range_extraction_regex = models.JSONField(blank=True)
    ignored_words = models.JSONField(blank=True)
    space_pixels = models.IntegerField()
    replace_results = models.JSONField(blank=True)

    def __str__(self):
        return self.name


class AnalysisCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AnalysisCategoryName(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "AnalysisCategory", on_delete=models.CASCADE, related_name="names"
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    pass


class AbstractPDF(models.Model):
    provider = models.ForeignKey(
        "AnalysisProvider",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AnalysisPDF(AbstractPDF):
    file = models.FileField(upload_to="analize-pdfs/")

    def __str__(self):
        return self.file.name


class RadiographyPDF(AbstractPDF):
    file = models.FileField(upload_to="radiografie-pdfs/")

    def __str__(self):
        return self.file.name


class Analysis(models.Model):
    source = models.OneToOneField(
        AnalysisPDF,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Analysis"
        verbose_name_plural = "Analyses"


class AnalysisResult(models.Model):
    category = models.ForeignKey(
        "AnalysisCategory", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    result = models.CharField(max_length=30)
    measurement_unit = models.CharField(max_length=10)
    refference_range = models.CharField(max_length=255)
    range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    in_range = models.BooleanField(null=True)
    suggestion = models.TextField(blank=True)

    analysis = models.ForeignKey(
        Analysis, on_delete=models.CASCADE, related_name="results"
    )
