from django.contrib import admin
from staff.models import Group, Division, Employee, Location
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "group_name"]

    list_display_links = ["group_name"]

    ordering = ["group_name"]


class DivisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "division_name"]

    list_display_links = ["division_name"]

    ordering = ["division_name"]


class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "last_name",
        "first_name",
        "email",
        "division",
        "group",
    ]

    list_display_links = ["id", "last_name", "first_name"]

    ordering = ["last_name", "first_name", "id"]


class LocationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "location_name"]

    list_display_links = ["location_name"]

    ordering = ["location_name"]


admin.site.register(Group, GroupAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Location, LocationAdmin)
