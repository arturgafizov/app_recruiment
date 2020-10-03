from django.contrib import admin
from .models import Specialty, Application, Company


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Company, CompanyAdmin)
