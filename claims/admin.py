from django.contrib import admin
from .models import Category, Claim, ClaimAuditLog, ClaimDocument, CoveragePlan, CoverageRule, EstablishmentPaymentOption, Hospital, IPM, IPMPaymentOption, NotificationLog, Patient, PaymentMethod


@admin.register(IPM)
class IPMAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city", "phone", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "city", "email")


@admin.register(CoveragePlan)
class CoveragePlanAdmin(admin.ModelAdmin):
    list_display = ("name", "ipm", "annual_ceiling", "is_active", "created_at")
    list_filter = ("ipm", "is_active")
    search_fields = ("name", "ipm__name")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "member_number", "ipm", "coverage_plan", "beneficiary_type", "phone", "created_at")
    search_fields = ("full_name", "member_number", "phone")
    list_filter = ("ipm", "beneficiary_type")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "method_type", "is_active", "created_at")
    list_filter = ("method_type", "is_active")
    search_fields = ("name", "code")


@admin.register(IPMPaymentOption)
class IPMPaymentOptionAdmin(admin.ModelAdmin):
    list_display = ("ipm", "payment_method", "phone", "iban", "bank_name", "payee_name", "is_active")
    list_filter = ("ipm", "payment_method", "is_active")
    search_fields = ("ipm__name", "payment_method__name", "phone", "iban", "payee_name")


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "is_deleted", "created_at")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("name", "code")


@admin.register(EstablishmentPaymentOption)
class EstablishmentPaymentOptionAdmin(admin.ModelAdmin):
    list_display = ("hospital", "payment_method", "phone", "iban", "bank_name", "payee_name", "is_active")
    list_filter = ("hospital", "payment_method", "is_active")
    search_fields = ("hospital__name", "payment_method__name", "phone", "iban", "payee_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_pharmacy", "is_active")
    list_filter = ("is_pharmacy", "is_active")


@admin.register(CoverageRule)
class CoverageRuleAdmin(admin.ModelAdmin):
    list_display = ("coverage_plan", "category", "coverage_percent", "is_active")
    list_filter = ("coverage_plan__ipm", "is_active")


class ClaimDocumentInline(admin.TabularInline):
    model = ClaimDocument
    extra = 0


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "provider", "status", "total_amount", "created_at")
    list_filter = ("status", "patient__ipm")
    search_fields = ("patient__full_name", "patient__member_number", "provider__username")
    inlines = [ClaimDocumentInline]


@admin.register(ClaimAuditLog)
class ClaimAuditLogAdmin(admin.ModelAdmin):
    list_display = ("claim", "actor", "event", "created_at")
    list_filter = ("event",)
    search_fields = ("claim__id", "actor__username", "notes")


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("claim", "channel", "target", "status", "sent_at")
    list_filter = ("channel", "status")
