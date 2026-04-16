from django.contrib import admin
from options.models import Version, PayrollInfo
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class VersionAdmin(admin.ModelAdmin):
    list_display = ["version_number"]

    list_display_links = ["version_number"]

    ordering = ["version_number"]

    def has_add_permission(self, request):
        # Return False to disable adding
        return False

    def has_delete_permission(self, request, obj=None):
        # Return False to disable deleting
        return False

    def has_change_permission(self, request, obj=None):
        # Return False to disable editing
        return False


class PayrollInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["payroll_year"]

    list_display_links = ["payroll_year"]

    ordering = ["payroll_year"]


admin.site.register(Version, VersionAdmin)
admin.site.register(PayrollInfo, PayrollInfoAdmin)
