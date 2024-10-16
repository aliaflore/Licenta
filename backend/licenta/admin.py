from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from licenta.models import AnalysisCategory, AnalysisCategoryName, AnalysisProvider, User, AnalysisPDF, RadiographyPDF, Analysis, AnalysisResult


class AnalysisProviderAdmin(admin.ModelAdmin):
    pass


class AnalysisCategoryAdmin(admin.ModelAdmin):
    pass


class AnalysisCategoryNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


class UserAdmin(BaseUserAdmin):
    pass


class AnalysisPDFAdmin(admin.ModelAdmin):
    pass


class RadiographyPdfAdmin(admin.ModelAdmin):
    pass


class AnalysisResultInline(admin.TabularInline):
    model = AnalysisResult


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'source']
    inlines = [AnalysisResultInline]


class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'result', 'measurement_unit', 'refference_range', 'range_min', 'range_max', 'in_range', 'analysis_link']
    readonly_fields = ['analysis_link']

    def analysis_link(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (reverse("admin:licenta_analysis_change", args=(obj.analysis.pk,)) , escape(obj)))

    analysis_link.allow_tags = True
    analysis_link.short_description = "Analysis"



admin.site.register(AnalysisProvider, AnalysisProviderAdmin)
admin.site.register(AnalysisCategory, AnalysisCategoryAdmin)
admin.site.register(AnalysisCategoryName, AnalysisCategoryNameAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AnalysisPDF, AnalysisPDFAdmin)
admin.site.register(RadiographyPDF, RadiographyPdfAdmin)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(AnalysisResult, AnalysisResultAdmin)
