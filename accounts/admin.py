from django.contrib import admin

from .models import StaffProfile


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "ipm", "ipm_name", "hospital", "organisation_name")
    list_filter = ("role", "ipm")
    search_fields = ("user__username", "user__email", "ipm__name", "ipm_name")
    autocomplete_fields = ["ipm", "hospital", "deleted_by"]

    fieldsets = (
        (None, {
            "fields": ("user", "role"),
        }),
        ("IPM", {
            "fields": ("ipm", "ipm_name"),
            "description": "Institution de prévoyance maladie (pour rôle IPM Admin).",
        }),
        ("Établissement", {
            "fields": ("hospital", "organisation_name"),
        }),
        ("Suppression (soft delete)", {
            "fields": ("is_deleted", "deleted_at", "deleted_by"),
            "classes": ("collapse",),
        }),
    )
