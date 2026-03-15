from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DemoRequest, DemoRequestNotificationConfig, Testimonial


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "organisation",
        "profile",
        "status",
        "created_at",
    )
    list_filter = ("status", "profile", "created_at")
    search_fields = ("first_name", "last_name", "email", "organisation", "message")
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "phone", "organisation", "profile", "message")}),
        ("Suivi", {"fields": ("status", "notes", "created_at")}),
    )


@admin.register(DemoRequestNotificationConfig)
class DemoRequestNotificationConfigAdmin(admin.ModelAdmin):
    list_display = ("__str__", "recipient_count", "send_copy_to_client", "updated_at")
    readonly_fields = ("updated_at",)
    fieldsets = (
        (
            "Qui reçoit les nouvelles demandes de démo ?",
            {
                "fields": ("notification_emails",),
                "description": "Indiquez une adresse email par ligne. Ces destinataires recevront un email à chaque nouvelle demande de démo. Si vide, les adresses de la variable d'environnement REMEDY_DEMO_NOTIFICATION_EMAILS seront utilisées.",
            },
        ),
        (
            "Confirmation au client",
            {
                "fields": ("send_copy_to_client",),
                "description": "Si activé, la personne qui soumet le formulaire recevra un email de confirmation.",
            },
        ),
        (None, {"fields": ("updated_at",)}),
    )

    def recipient_count(self, obj):
        count = len(obj.get_recipient_list())
        return f"{count} adresse(s)" if count else "—"
    recipient_count.short_description = "Destinataires"

    def has_add_permission(self, request):
        return not DemoRequestNotificationConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirige vers l'unique objet de configuration s'il existe."""
        obj = DemoRequestNotificationConfig.objects.first()
        if obj:
            return HttpResponseRedirect(reverse("admin:core_demorequestnotificationconfig_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "role_or_organisation", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("author", "role_or_organisation", "quote")
    ordering = ("order", "created_at")
    fieldsets = (
        (None, {"fields": ("author", "role_or_organisation", "quote")}),
        ("Publication", {"fields": ("order", "is_active")}),
        (None, {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at",)
