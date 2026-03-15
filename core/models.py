from django.db import models


class DemoRequest(models.Model):
    """Demande de démo envoyée depuis la landing page."""

    PROFILE_CHOICES = [
        ("ipm", "IPM / Mutuelle"),
        ("prestataire", "Prestataire de soins (Médecin, Clinique, Pharmacie)"),
        ("patient", "Patient / Assuré"),
        ("partenaire", "Partenaire"),
        ("autre", "Autre"),
    ]

    STATUS_CHOICES = [
        ("new", "Nouvelle"),
        ("contacted", "Contactée"),
        ("done", "Traitée"),
    ]

    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email professionnel")
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    organisation = models.CharField("Organisation", max_length=255)
    profile = models.CharField("Profil", max_length=20, choices=PROFILE_CHOICES)
    message = models.TextField("Besoin / message", blank=True)
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )
    created_at = models.DateTimeField("Date de demande", auto_now_add=True)
    notes = models.TextField("Notes interne (admin)", blank=True)

    class Meta:
        verbose_name = "Demande de démo"
        verbose_name_plural = "Demandes de démo"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} – {self.organisation} ({self.get_profile_display()})"


class DemoRequestNotificationConfig(models.Model):
    """
    Configuration des notifications pour les demandes de démo (singleton).
    Permet à l'équipe Remedi de définir qui reçoit les alertes et si le client reçoit une copie.
    """
    notification_emails = models.TextField(
        "Adresses qui reçoivent les nouvelles demandes",
        blank=True,
        help_text="Une adresse email par ligne. Laissez vide pour utiliser les adresses définies dans la variable d'environnement REMEDY_DEMO_NOTIFICATION_EMAILS.",
    )
    send_copy_to_client = models.BooleanField(
        "Envoyer une copie de confirmation au client",
        default=False,
        help_text="Si coché, la personne qui soumet la demande reçoit un email de confirmation.",
    )
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        verbose_name = "Configuration des notifications démo"
        verbose_name_plural = "Configuration des notifications démo"

    def __str__(self):
        return "Notifications demandes de démo"

    def get_recipient_list(self):
        """Retourne la liste des adresses (une par ligne), nettoyée."""
        if not self.notification_emails or not self.notification_emails.strip():
            return []
        return [e.strip() for e in self.notification_emails.strip().splitlines() if e.strip()]


class Testimonial(models.Model):
    """Avis / témoignage affiché sur la landing (section « Ils nous font confiance »)."""
    author = models.CharField("Auteur", max_length=120)
    role_or_organisation = models.CharField(
        "Fonction ou organisation",
        max_length=255,
        help_text="Ex. : Directrice des opérations, IPM Horizon Santé — ou : Clinique de l'Espoir",
    )
    quote = models.TextField("Citation / avis")
    order = models.PositiveIntegerField("Ordre d'affichage", default=0, help_text="Plus le nombre est petit, plus l'avis apparaît en premier.")
    is_active = models.BooleanField("Publié", default=True)
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)

    class Meta:
        verbose_name = "Avis / Témoignage"
        verbose_name_plural = "Avis / Témoignages"
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.author} – {self.role_or_organisation}"


class EmailLog(models.Model):
    """Log de tous les emails envoyés par le système (statut, contenu, possibilité de renvoi)."""
    STATUS_CHOICES = [
        ("sent", "Envoyé"),
        ("failed", "Échec"),
    ]
    EMAIL_TYPE_CHOICES = [
        ("demo_team", "Démo – notification équipe"),
        ("demo_client", "Démo – confirmation client"),
        ("claim_notification", "Réclamation – lien validation patient"),
        ("test", "Test"),
        ("resend", "Renvoi"),
        ("other", "Autre"),
    ]

    to_emails = models.TextField("Destinataires")  # séparés par des virgules
    from_email = models.CharField("Expéditeur", max_length=255)
    subject = models.CharField("Objet", max_length=500)
    body_plain = models.TextField("Corps (texte)", blank=True)
    body_html = models.TextField("Corps (HTML)", blank=True)
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField("Date d'envoi", auto_now_add=True)
    error_message = models.TextField("Message d'erreur", blank=True)
    email_type = models.CharField("Type", max_length=50, blank=True)
    related_ref = models.CharField("Référence", max_length=255, blank=True, help_text="Ex. demorequest:5, claim:123")

    class Meta:
        verbose_name = "Log d'email"
        verbose_name_plural = "Logs d'emails"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.subject[:50]} → {self.to_emails[:50]} ({self.status})"

    def get_to_list(self):
        return [e.strip() for e in self.to_emails.split(",") if e.strip()]

    def get_email_type_display(self):
        d = dict(self.EMAIL_TYPE_CHOICES)
        return d.get(self.email_type) or self.email_type or "—"
