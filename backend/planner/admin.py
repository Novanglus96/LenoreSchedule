from django.contrib import admin
from planner.models import Holiday
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class HolidayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "holiday_name"]

    list_display_links = ["holiday_name"]

    ordering = ["holiday_name"]


admin.site.register(Holiday, HolidayAdmin)
