from django.contrib import admin
from staff.models import Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class GroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "group_name"]

    list_display_links = ["group_name"]

    ordering = ["group_name"]


admin.site.register(Group, GroupAdmin)
