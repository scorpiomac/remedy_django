from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager qui exclut les enregistrements soft-deleted par défaut."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteMixin(models.Model):
    """Mixin pour soft delete : is_deleted, deleted_at, deleted_by. delete() marque comme supprimé."""

    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé (soft)")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date suppression")
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Supprimé par",
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        update_fields = ["is_deleted", "deleted_at"]
        if hasattr(self, "deleted_by_id"):
            update_fields.append("deleted_by")
        self.save(update_fields=update_fields)


class IPM(SoftDeleteMixin, models.Model):
    """Institution de Prévoyance Maladie : organisme d'assurance santé. Suppression = soft delete."""

    name = models.CharField(max_length=120, verbose_name="Raison sociale / Nom")
    code = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Code (ex: SANTEPLUS)",
        help_text="Identifiant court pour référence",
    )
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse siège")
    city = models.CharField(max_length=80, blank=True, verbose_name="Ville")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "IPM"
        verbose_name_plural = "IPMs"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(is_deleted=False),
                name="unique_ipm_name_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["code"],
                condition=Q(is_deleted=False) & ~Q(code=""),
                name="unique_ipm_code_not_deleted",
            ),
        ]

    def __str__(self):
        return self.name


class EstablishmentType(models.TextChoices):
    HOSPITAL = "HOSPITAL", "Hôpital / Clinique"
    PHARMACY = "PHARMACY", "Pharmacie"


class Hospital(SoftDeleteMixin, models.Model):
    """Hôpital, clinique ou pharmacie : prestataire de soins. Même structure qu'IPM (coordonnées complètes). Suppression = soft delete."""

    establishment_type = models.CharField(
        max_length=20,
        choices=EstablishmentType.choices,
        default=EstablishmentType.HOSPITAL,
        verbose_name="Type",
    )
    name = models.CharField(max_length=120, verbose_name="Raison sociale / Nom")
    code = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Code",
        help_text="Identifiant court pour référence",
    )
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=80, blank=True, verbose_name="Ville")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hôpital / Pharmacie"
        verbose_name_plural = "Hôpitaux / Pharmacies"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(is_deleted=False),
                name="unique_hospital_name_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["code"],
                condition=Q(is_deleted=False) & ~Q(code=""),
                name="unique_hospital_code_not_deleted",
            ),
        ]

    def __str__(self):
        return self.name


class BeneficiaryType(models.TextChoices):
    TITULAIRE = "TITULAIRE", "Titulaire (adhérent principal)"
    CONJOINT = "CONJOINT", "Conjoint(e)"
    ENFANT = "ENFANT", "Enfant"
    AYANT_DROIT = "AYANT_DROIT", "Ayant droit"


class Gender(models.TextChoices):
    M = "M", "Masculin"
    F = "F", "Féminin"
    OTHER = "OTHER", "Autre"


class CoveragePlan(models.Model):
    """Formule de couverture proposee par une IPM (ex: Formule Excellence, Formule Standard)."""

    ipm = models.ForeignKey(IPM, on_delete=models.PROTECT, related_name="plans")
    name = models.CharField(max_length=150, help_text="Nom de la formule (ex: Formule A 80%)")
    annual_ceiling = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Plafond annuel en FCFA (laisser vide = illimite)",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ipm", "name"], name="unique_plan_per_ipm"),
        ]

    def __str__(self):
        return f"{self.ipm.name} - {self.name}"


class Patient(models.Model):
    """Bénéficiaire / assuré : identité, contact, adresse, couverture."""

    ipm = models.ForeignKey(IPM, on_delete=models.PROTECT, related_name="patients")
    coverage_plan = models.ForeignKey(
        CoveragePlan,
        on_delete=models.PROTECT,
        related_name="patients",
        null=True,
        blank=True,
        help_text="Formule de couverture du patient",
    )
    beneficiary_type = models.CharField(
        max_length=20,
        choices=BeneficiaryType.choices,
        default=BeneficiaryType.TITULAIRE,
    )
    # Identité
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de naissance",
        help_text="Format JJ/MM/AAAA",
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        verbose_name="Genre",
    )
    id_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="N° CNI / pièce d'identité",
        help_text="Numéro de CNI ou passeport. Utilisé pour la recherche chez les providers.",
    )
    id_document = models.FileField(
        upload_to="patient_kyc/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Photo / scan pièce d'identité (KYC)",
        help_text="Recto ou recto-verso de la CNI, passeport, etc.",
    )
    # Contact
    phone = models.CharField(max_length=30, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    # Adresse
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=80, blank=True, verbose_name="Ville")
    # Adhésion
    member_number = models.CharField(max_length=80, verbose_name="N° membre / matricule")
    notes = models.TextField(blank=True, verbose_name="Remarques")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ipm", "member_number"], name="unique_patient_per_ipm"),
        ]
        verbose_name = "Patient / Bénéficiaire"
        verbose_name_plural = "Patients / Bénéficiaires"

    def __str__(self):
        return f"{self.full_name} - {self.member_number}"


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    is_pharmacy = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PaymentMethodType(models.TextChoices):
    """Type de moyen de paiement : détermine quels champs afficher (tél, IBAN, etc.)."""
    MOBILE_MONEY = "MOBILE_MONEY", "Mobile money"
    VIREMENT = "VIREMENT", "Virement bancaire"
    CHEQUE = "CHEQUE", "Chèque"
    ESPECES = "ESPECES", "Espèces"
    CARTE = "CARTE", "Carte bancaire"
    OTHER = "OTHER", "Autre"


class PaymentMethod(models.Model):
    """Moyen de paiement (virement, chèque, espèces, mobile money, etc.)."""

    name = models.CharField(max_length=80, unique=True, verbose_name="Libellé")
    code = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Code",
        help_text="Ex: VIREMENT, MOBILE_MONEY",
    )
    method_type = models.CharField(
        max_length=20,
        choices=PaymentMethodType.choices,
        default=PaymentMethodType.OTHER,
        verbose_name="Type",
        help_text="Définit les champs à renseigner (tél, IBAN, bénéficiaire…)",
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Moyen de paiement"
        verbose_name_plural = "Moyens de paiement"
        ordering = ["name"]

    def __str__(self):
        return self.name


class IPMPaymentOption(SoftDeleteMixin, models.Model):
    """Moyen de paiement accepté par une IPM, avec infos spécifiques (tél, IBAN, etc.)."""

    ipm = models.ForeignKey(IPM, on_delete=models.CASCADE, related_name="payment_options")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name="ipm_options")
    # Champs selon type : Mobile money → phone ; Virement → iban, bank_name ; Chèque → payee_name
    phone = models.CharField(max_length=30, blank=True, verbose_name="N° téléphone (mobile money)")
    iban = models.CharField(max_length=40, blank=True, verbose_name="IBAN")
    bank_name = models.CharField(max_length=120, blank=True, verbose_name="Banque")
    payee_name = models.CharField(max_length=120, blank=True, verbose_name="À l'ordre de (chèque)")
    reference_notes = models.CharField(max_length=255, blank=True, verbose_name="Référence / précisions")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Moyen de paiement IPM"
        verbose_name_plural = "Moyens de paiement IPM"
        constraints = [
            models.UniqueConstraint(
                fields=["ipm", "payment_method"],
                name="unique_ipm_payment_option",
                condition=models.Q(is_deleted=False),
            ),
        ]
        ordering = ["payment_method__name"]

    def __str__(self):
        return f"{self.ipm.name} — {self.payment_method.name}"


class EstablishmentPaymentOption(SoftDeleteMixin, models.Model):
    """Moyen de paiement configuré pour un établissement (hôpital, clinique, pharmacie). Visible par l'IPM sur la fiche réclamation pour payer le prestataire."""

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="payment_options"
    )
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="establishment_options"
    )
    phone = models.CharField(max_length=30, blank=True, verbose_name="N° téléphone (mobile money)")
    iban = models.CharField(max_length=40, blank=True, verbose_name="IBAN")
    bank_name = models.CharField(max_length=120, blank=True, verbose_name="Banque")
    payee_name = models.CharField(max_length=120, blank=True, verbose_name="À l'ordre de (chèque)")
    reference_notes = models.CharField(max_length=255, blank=True, verbose_name="Référence / précisions")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Moyen de paiement établissement"
        verbose_name_plural = "Moyens de paiement établissement"
        constraints = [
            models.UniqueConstraint(
                fields=["hospital", "payment_method"],
                name="unique_establishment_payment_option",
                condition=models.Q(is_deleted=False),
            ),
        ]
        ordering = ["payment_method__name"]

    def __str__(self):
        return f"{self.hospital.name} — {self.payment_method.name}"


class CoverageRule(models.Model):
    coverage_plan = models.ForeignKey(
        CoveragePlan,
        on_delete=models.PROTECT,
        related_name="rules",
        null=True,
        blank=True,
        help_text="Formule de couverture",
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="coverage_rules")
    coverage_percent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["coverage_plan", "category"], name="unique_coverage_per_plan_category"),
        ]

    def __str__(self):
        return f"{self.coverage_plan} / {self.category} ({self.coverage_percent}%)"


class ClaimStatus(models.TextChoices):
    DRAFT = "DRAFT", "Brouillon"
    SUBMITTED = "SUBMITTED", "Soumise"
    LOCKED = "LOCKED", "Verrouillée"
    PATIENT_CONFIRMED = "PATIENT_CONFIRMED", "Confirmée patient"
    READY_FOR_PAYMENT = "READY_FOR_PAYMENT", "Prête au paiement"
    DISPUTED = "DISPUTED", "Contestée"
    BLOCKED = "BLOCKED", "Bloquée"


class Claim(SoftDeleteMixin, models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="claims")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="claims")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="claims")
    status = models.CharField(max_length=25, choices=ClaimStatus.choices, default=ClaimStatus.DRAFT)
    care_date = models.DateField(null=True, blank=True, help_text="Date des soins")
    invoice_number = models.CharField(max_length=80, blank=True, help_text="N° facture / référence")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    medicine_names = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    snapshot_json = models.JSONField(default=dict, blank=True)
    patient_token = models.CharField(max_length=128, null=True, blank=True, unique=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    token_used_at = models.DateTimeField(null=True, blank=True)
    block_reason = models.CharField(max_length=255, blank=True)
    dispute_reason = models.TextField(blank=True, verbose_name="Motif de contestation (patient)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Claim #{self.id} - {self.status}"


class DocumentType(models.TextChoices):
    ORDONNANCE = "ORDONNANCE", "Ordonnance"
    FACTURE = "FACTURE", "Facture"
    BON_PRISE_EN_CHARGE = "BON_PRISE_EN_CHARGE", "Bon de prise en charge"
    RESULTAT_LABO = "RESULTAT_LABO", "Résultat laboratoire"
    AUTRE = "AUTRE", "Autre"


class ClaimDocument(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="claim_documents/%Y/%m/%d")
    original_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=25, choices=DocumentType.choices, default=DocumentType.AUTRE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ClaimAuditLog(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="audit_logs")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.CharField(max_length=80)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class NotificationChannel(models.TextChoices):
    SMS = "SMS", "SMS"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    EMAIL = "EMAIL", "Email"


class NotificationChannelConfig(models.Model):
    """Configuration par canal (Email, SMS, WhatsApp) : actif/inactif, paramètres, dernier test."""
    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        unique=True,
        verbose_name="Canal",
    )
    is_active = models.BooleanField(default=False, verbose_name="Actif")
    config = models.JSONField(default=dict, blank=True, verbose_name="Paramètres (JSON)")
    last_tested_at = models.DateTimeField(null=True, blank=True, verbose_name="Dernier test")
    last_test_error = models.TextField(blank=True, verbose_name="Erreur dernier test")

    class Meta:
        verbose_name = "Configuration notification"
        verbose_name_plural = "Configurations notifications"
        ordering = ["channel"]

    def __str__(self):
        return f"{self.get_channel_display()} ({'actif' if self.is_active else 'inactif'})"


class NotificationLog(models.Model):
    """Historique des envois (email, SMS, WhatsApp) vers le patient avec statut et possibilité de renvoyer."""
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="notification_logs")
    channel = models.CharField(max_length=20, choices=NotificationChannel.choices)
    target = models.CharField(max_length=255, help_text="Email, numéro de téléphone, etc.")
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="SENT")  # SENT, FAILED
    error_message = models.TextField(blank=True, verbose_name="Message d'erreur (si échec)")
