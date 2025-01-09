from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import functools
from encrypted_model_fields.fields import EncryptedTextField, EncryptedDateField, EncryptedMixin, EncryptedBooleanField


class EncryptedDecimalField(EncryptedMixin, models.DecimalField):
    pass


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

    analysis_list = models.URLField(blank=True)
    analysis_providedlang = models.TextField(choices=settings.LANGUAGES, default="en")
    analysis_list_skip_first_row = models.BooleanField(default=False)
    analysis_list_skip_first_table = models.BooleanField(default=False)
    analysis_columns = models.JSONField(default=functools.partial(list, [0, 1, 2, 3]))

    def __str__(self):
        return self.name


class AnalysisCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AnalysisCategoryName(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "AnalysisCategory", on_delete=models.CASCADE, related_name="related_names"
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

    taken_on = EncryptedDateField(null=True)
    doctor_notes = EncryptedTextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AnalysisPDF(AbstractPDF):
    file = models.FileField(upload_to="analize-pdfs/")

    suggestion = EncryptedTextField(blank=True)

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

    notes = EncryptedTextField(blank=True)
    date = EncryptedDateField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Analysis"
        verbose_name_plural = "Analyses"


class AnalysisResult(models.Model):
    category = models.ForeignKey(
        "AnalysisCategory", on_delete=models.CASCADE
    )
    name = EncryptedTextField(max_length=50)
    result = EncryptedTextField(max_length=30)
    measurement_unit = EncryptedTextField(max_length=10)
    refference_range = EncryptedTextField(max_length=255)
    range_min = EncryptedDecimalField(max_digits=10, decimal_places=2, null=True)
    range_max = EncryptedDecimalField(max_digits=10, decimal_places=2, null=True)
    in_range = EncryptedBooleanField(null=True)
    suggestion = EncryptedTextField(blank=True)

    doctor_note = EncryptedTextField(blank=True)

    analysis = models.ForeignKey(
        Analysis, on_delete=models.CASCADE, related_name="results"
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Translation(models.Model):
    original_text = models.TextField(db_index=True)
    translated_text = models.TextField()
    source_language = models.TextField(choices=settings.LANGUAGES, default="en")
    target_language = models.TextField(choices=settings.LANGUAGES, default="ro")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class ExtraAnalysisCategories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name