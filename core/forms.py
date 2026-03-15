from django import forms
from .models import DemoRequest, DemoRequestNotificationConfig, Testimonial


class DemoRequestForm(forms.ModelForm):
    """Formulaire de demande de démo (landing)."""

    class Meta:
        model = DemoRequest
        fields = ("first_name", "last_name", "email", "phone", "organisation", "profile", "message")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Jean", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Dupont", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all"}),
            "email": forms.EmailInput(attrs={"placeholder": "jean@organisation.com", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all"}),
            "phone": forms.TextInput(attrs={"placeholder": "+221 77 000 00 00", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all"}),
            "organisation": forms.TextInput(attrs={"placeholder": "Nom de votre structure", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all"}),
            "profile": forms.Select(attrs={"class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all appearance-none"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Décrivez brièvement votre besoin...", "class": "w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-remedy-teal focus:border-remedy-teal outline-none transition-all resize-none"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["message"].required = False
        self.fields["profile"].choices = [("", "Sélectionnez un profil")] + list(DemoRequest.PROFILE_CHOICES)


class DemoRequestBackofficeForm(forms.ModelForm):
    """Formulaire backoffice : statut et notes pour une demande de démo."""

    class Meta:
        model = DemoRequest
        fields = ("status", "notes")
        widgets = {
            "status": forms.Select(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm"}),
            "notes": forms.Textarea(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm", "rows": 4, "placeholder": "Notes de suivi..."}),
        }


class TestimonialForm(forms.ModelForm):
    """Formulaire backoffice pour les avis / témoignages (landing)."""

    class Meta:
        model = Testimonial
        fields = ("author", "role_or_organisation", "quote", "order", "is_active")
        widgets = {
            "author": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm", "placeholder": "Ex. : Aminata Diallo"}),
            "role_or_organisation": forms.TextInput(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm", "placeholder": "Ex. : Directrice des opérations, IPM Horizon Santé"}),
            "quote": forms.Textarea(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm", "rows": 4, "placeholder": "Citation affichée sur la page d'accueil..."}),
            "order": forms.NumberInput(attrs={"class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm", "min": 0}),
            "is_active": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"}),
        }


class DemoRequestNotificationConfigForm(forms.ModelForm):
    """Formulaire backoffice : qui reçoit les mails de demande de démo."""

    class Meta:
        model = DemoRequestNotificationConfig
        fields = ("notification_emails", "send_copy_to_client")
        widgets = {
            "notification_emails": forms.Textarea(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm font-mono text-sm",
                    "rows": 8,
                    "placeholder": "contact@remediafrica.com\ncommercial@remediafrica.com",
                }
            ),
            "send_copy_to_client": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"}),
        }
        labels = {
            "notification_emails": "Adresses qui reçoivent les nouvelles demandes de démo",
            "send_copy_to_client": "Envoyer une copie de confirmation au client",
        }
        help_texts = {
            "notification_emails": "Une adresse email par ligne. Ces personnes recevront un email à chaque nouvelle demande de démo.",
            "send_copy_to_client": "Si coché, la personne qui remplit le formulaire reçoit un email de confirmation.",
        }
