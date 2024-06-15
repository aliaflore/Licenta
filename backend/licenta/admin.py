from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from licenta.models import User, AnalizePDF, RadiografiePDF, Analize, AnalizeRezultate


class UserAdmin(BaseUserAdmin):
    pass


class AnalizePDFAdmin(admin.ModelAdmin):
    pass


class RadiografiePdfAdmin(admin.ModelAdmin):
    pass


class AnalizeAdmin(admin.ModelAdmin):
    pass


class AnalizeRezultateAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(AnalizePDF, AnalizePDFAdmin)
admin.site.register(RadiografiePDF, RadiografiePdfAdmin)
admin.site.register(Analize, AnalizeAdmin)
admin.site.register(AnalizeRezultate, AnalizeRezultateAdmin)
