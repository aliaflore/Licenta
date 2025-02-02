from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from licenta.models import AnalysisCategory, AnalysisCategoryName, AnalysisProvider, ExtraAnalysisCategories, Translation, User, AnalysisPDF, RadiographyPDF, Analysis, AnalysisResult, PatientInvite
from django.utils.translation import gettext_lazy as _


class AnalysisProviderAdmin(admin.ModelAdmin):
    pass


class AnalysisCategoryAdmin(admin.ModelAdmin):
    pass


class AnalysisCategoryNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Doctor Information"), {"fields": ("is_doctor", "doctor_proof")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "is_doctor")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_doctor")


class AnalysisPDFAdmin(admin.ModelAdmin):
    pass


class RadiographyPdfAdmin(admin.ModelAdmin):
    pass


class AnalysisResultInline(admin.TabularInline):
    model = AnalysisResult


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'source']


class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'result', 'measurement_unit', 'refference_range', 'range_min', 'range_max', 'in_range', 'analysis_link']
    readonly_fields = ['analysis_link']

    def analysis_link(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (reverse("admin:licenta_analysis_change", args=(obj.analysis.pk,)) , escape(obj)))

    analysis_link.allow_tags = True
    analysis_link.short_description = "Analysis"


class PatientInviteAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'accepted']

class TranslationAdmin(admin.ModelAdmin):
    list_display = ['original_text', 'translated_text', 'source_language', 'target_language']


admin.site.register(AnalysisProvider, AnalysisProviderAdmin)
admin.site.register(AnalysisCategory, AnalysisCategoryAdmin)
admin.site.register(AnalysisCategoryName, AnalysisCategoryNameAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AnalysisPDF, AnalysisPDFAdmin)
admin.site.register(RadiographyPDF, RadiographyPdfAdmin)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(AnalysisResult, AnalysisResultAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(ExtraAnalysisCategories)
admin.site.register(PatientInvite, PatientInviteAdmin)

