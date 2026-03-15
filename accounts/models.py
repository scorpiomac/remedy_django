from django.conf import settings
from django.db import models

from claims.models import SoftDeleteMixin


class UserRole(models.TextChoices):
    SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Admin"
    IPM_ADMIN = "IPM_ADMIN", "IPM Admin"
    DOCTOR = "DOCTOR", "Doctor"
    PHARMACY = "PHARMACY", "Pharmacy"


class StaffProfile(SoftDeleteMixin, models.Model):
    """Profil métier (rôle, IPM, nom d'organisation pour prestataires). Suppression = soft delete ; désactive aussi l'utilisateur (is_active=False)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.DOCTOR)
    ipm = models.ForeignKey(
        "claims.IPM",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="staff_profiles",
        verbose_name="IPM",
        help_text="Institution de prévoyance maladie (pour rôle IPM Admin). Utilisé pour le périmètre des dossiers et patients.",
    )
    ipm_name = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Nom IPM",
        help_text="Nom de l'IPM (affiché). Synchronisé avec la FK IPM si elle est renseignée.",
    )
    hospital = models.ForeignKey(
        "claims.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_profiles",
        verbose_name="Hôpital / Pharmacie",
        help_text="Établissement de soins (prestataire). Affiché sur la page de validation patient.",
    )
    organisation_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nom de l'organisation (legacy)",
        help_text="Ancien champ texte ; préférer l’objet Hôpital si renseigné.",
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def get_ipm_display_name(self):
        """Nom de l'IPM pour affichage (compatible ancien modèle sans champ ipm)."""
        ipm = getattr(self, "ipm", None)
        if ipm:
            return ipm.name
        return (getattr(self, "ipm_name", None) or "").strip() or "—"

    def delete(self, *args, **kwargs):
        """Soft delete + désactivation du compte utilisateur."""
        super().delete(*args, **kwargs)
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
