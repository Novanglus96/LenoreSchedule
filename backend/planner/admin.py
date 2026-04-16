from django.contrib import admin
from planner.models import Holiday, CalendarEntry, ScheduleTemplate
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class HolidayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "holiday_name"]

    list_display_links = ["holiday_name"]

    ordering = ["holiday_name"]


class CalendarEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "calendar_date",
        "entry_type",
        "start_time",
        "end_time",
        "employee",
        "location",
        "confirmed",
    ]

    list_display_links = ["calendar_date"]

    ordering = ["calendar_date", "employee", "start_time", "end_time"]


class ScheduleTemplateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "day_of_week",
        "start_time",
        "end_time",
        "location",
    ]

    list_display_links = ["employee"]

    ordering = ["employee", "day_of_week", "start_time"]


admin.site.register(Holiday, HolidayAdmin)
admin.site.register(CalendarEntry, CalendarEntryAdmin)
admin.site.register(ScheduleTemplate, ScheduleTemplateAdmin)
