from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q

from accounts.models import StaffProfile, UserRole
from .models import (
    BeneficiaryType,
    Category,
    Claim,
    CoveragePlan,
    CoverageRule,
    DocumentType,
    EstablishmentType,
    Hospital,
    IPM,
    NotificationChannel,
    NotificationChannelConfig,
    Patient,
    PaymentMethod,
    PaymentMethodType,
)


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ClaimCreateForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ["patient", "category", "care_date", "invoice_number", "total_amount", "medicine_names"]

        widgets = {
            "patient": forms.Select(attrs={"class": "block w-full"}),
            "category": forms.Select(attrs={"class": "block w-full"}),
            "care_date": forms.DateInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 pl-4 pr-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm caret-slate-900",
                    "type": "date",
                }
            ),
            "invoice_number": forms.TextInput(attrs={
                "class": "block w-full rounded-xl border border-slate-300 py-2.5 pl-4 pr-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm caret-slate-900",
                "placeholder": "N° facture ou référence",
            }),
            "total_amount": forms.NumberInput(attrs={
                "class": "flex-1 min-w-[140px] w-full border-0 py-2.5 pl-3 pr-4 text-slate-900 focus:ring-0 focus:outline-none sm:text-sm caret-slate-900",
                "step": "0.01",
                "min": "0",
                "placeholder": "0",
                "size": "12",
            }),
            "medicine_names": forms.Textarea(attrs={
                "class": "block w-full rounded-md border border-slate-300 py-1.5 pl-3 pr-3 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm placeholder:text-slate-400 caret-slate-900",
                "rows": 4,
                "placeholder": "Liste des médicaments ou prestations (obligatoire si pharmacie)...",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient"].queryset = Patient.objects.select_related("ipm", "coverage_plan").order_by("full_name")
        self.fields["category"].queryset = Category.objects.filter(is_active=True).order_by("name")
        self.fields["care_date"].required = True

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        medicine_names = (cleaned.get("medicine_names") or "").strip()
        if category and category.is_pharmacy and not medicine_names:
            self.add_error(
                "medicine_names",
                ValidationError("Les détails médicaments sont obligatoires pour les catégories pharmacie."),
            )
        return cleaned


class ClaimEditForm(ClaimCreateForm):
    pass


class ClaimDocumentUploadForm(forms.Form):
    document_type = forms.ChoiceField(
        choices=DocumentType.choices,
        widget=forms.Select(attrs={"class": "block w-full"}),
    )
    documents = forms.FileField(
        widget=MultiFileInput(attrs={
            "class": "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100",
            "multiple": True,
        }),
        required=True,
    )


class IPMForm(forms.ModelForm):
    class Meta:
        model = IPM
        fields = ["name", "code", "address", "city", "phone", "email", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "Raison sociale / Nom de l'organisme",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "Ex: SANTEPLUS",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "Adresse du siège",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "Ville",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "Téléphone",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                    "placeholder": "contact@ipm.sn",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"}),
        }


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ["establishment_type", "name", "code", "address", "city", "phone", "email", "is_active"]
        widgets = {
            "establishment_type": forms.Select(attrs={"class": "no-tom-select block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm"}),
            "name": forms.TextInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "Raison sociale / Nom"}),
            "code": forms.TextInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "Ex: CHU-DAKAR"}),
            "address": forms.TextInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "Adresse"}),
            "city": forms.TextInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "Ville"}),
            "phone": forms.TextInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "Téléphone"}),
            "email": forms.EmailInput(attrs={"class": "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm", "placeholder": "contact@exemple.sn"}),
            "is_active": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"}),
        }


# ---------- CoveragePlan (Formule) ----------
_INPUT_CLASS = "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm"
_CHECK_CLASS = "h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"


class CoveragePlanForm(forms.ModelForm):
    class Meta:
        model = CoveragePlan
        fields = ["ipm", "name", "annual_ceiling", "is_active"]
        widgets = {
            "ipm": forms.Select(attrs={"class": f"{_INPUT_CLASS} no-tom-select"}),
            "name": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Ex: Formule Excellence"}),
            "annual_ceiling": forms.NumberInput(attrs={
                "class": _INPUT_CLASS,
                "min": "0",
                "step": "0.01",
                "placeholder": "Laisser vide = illimité",
            }),
            "is_active": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        ipm_queryset = kwargs.pop("ipm_queryset", None)
        forced_ipm = kwargs.pop("forced_ipm", None)
        super().__init__(*args, **kwargs)
        self.forced_ipm = forced_ipm
        if ipm_queryset is not None:
            self.fields["ipm"].queryset = ipm_queryset
        else:
            self.fields["ipm"].queryset = IPM.objects.filter(is_active=True).order_by("name")
        if forced_ipm is not None:
            self.fields["ipm"].queryset = IPM.objects.filter(id=forced_ipm.id)
            self.fields["ipm"].initial = forced_ipm
            self.fields["ipm"].widget = forms.HiddenInput()

    def clean(self):
        cleaned = super().clean()
        if self.forced_ipm is not None:
            cleaned["ipm"] = self.forced_ipm
        return cleaned


# ---------- Patient ----------

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "ipm",
            "coverage_plan",
            "beneficiary_type",
            "full_name",
            "date_of_birth",
            "gender",
            "id_number",
            "id_document",
            "phone",
            "email",
            "address",
            "city",
            "member_number",
            "notes",
        ]
        widgets = {
            "ipm": forms.Select(attrs={"class": "block w-full no-tom-select"}),
            "coverage_plan": forms.Select(attrs={"class": "block w-full"}),
            "beneficiary_type": forms.Select(attrs={"class": "block w-full"}),
            "full_name": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Nom et prénom(s)"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": _INPUT_CLASS, "type": "date", "placeholder": "JJ/MM/AAAA"},
                format="%Y-%m-%d",
            ),
            "gender": forms.Select(attrs={"class": f"{_INPUT_CLASS} no-tom-select"}),
            "id_number": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "N° CNI ou passeport (recherche providers)"}),
            "id_document": forms.FileInput(attrs={"class": "block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-brand-50 file:px-4 file:py-2 file:text-brand-700 hover:file:bg-brand-100", "accept": "image/*,.pdf"}),
            "phone": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Ex: +221 77 123 45 67"}),
            "email": forms.EmailInput(attrs={"class": _INPUT_CLASS, "placeholder": "email@exemple.com"}),
            "address": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Adresse postale"}),
            "city": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Ville"}),
            "member_number": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "N° membre / matricule"}),
            "notes": forms.Textarea(attrs={"class": _INPUT_CLASS, "rows": 3, "placeholder": "Remarques éventuelles"}),
        }

    def __init__(self, *args, **kwargs):
        ipm_queryset = kwargs.pop("ipm_queryset", None)
        plan_queryset = kwargs.pop("plan_queryset", None)
        forced_ipm = kwargs.pop("forced_ipm", None)
        super().__init__(*args, **kwargs)
        qs = ipm_queryset if ipm_queryset is not None else IPM.objects.filter(is_active=True).order_by("name")
        self.fields["ipm"].queryset = qs
        if plan_queryset is not None:
            self.fields["coverage_plan"].queryset = plan_queryset.select_related("ipm").order_by("ipm__name", "name")
        else:
            self.fields["coverage_plan"].queryset = CoveragePlan.objects.filter(is_active=True).select_related("ipm").order_by("ipm__name", "name")
        self.fields["coverage_plan"].required = False
        self.forced_ipm = forced_ipm
        if forced_ipm is not None:
            self.fields["ipm"].initial = forced_ipm
            self.fields["ipm"].widget = forms.HiddenInput()
            self.fields["ipm"].queryset = IPM.objects.filter(pk=forced_ipm.pk)

    def clean(self):
        cleaned = super().clean()
        if self.forced_ipm is not None:
            cleaned["ipm"] = self.forced_ipm
        return cleaned


# ---------- CoverageRule ----------

class CoverageRuleForm(forms.ModelForm):
    class Meta:
        model = CoverageRule
        fields = ["coverage_plan", "category", "coverage_percent", "is_active"]
        widgets = {
            "coverage_plan": forms.Select(attrs={"class": "block w-full"}),
            "category": forms.Select(attrs={"class": "block w-full"}),
            "coverage_percent": forms.NumberInput(
                attrs={
                    "class": _INPUT_CLASS,
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                    "placeholder": "0 - 100",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        plan_queryset = kwargs.pop("plan_queryset", None)
        forced_plan = kwargs.pop("forced_plan", None)
        super().__init__(*args, **kwargs)
        self.forced_plan = forced_plan
        if plan_queryset is not None:
            self.fields["coverage_plan"].queryset = plan_queryset
        else:
            self.fields["coverage_plan"].queryset = CoveragePlan.objects.filter(is_active=True).select_related("ipm").order_by("ipm__name", "name")
        self.fields["category"].queryset = Category.objects.filter(is_active=True).order_by("name")
        if forced_plan is not None:
            self.fields["coverage_plan"].queryset = CoveragePlan.objects.filter(id=forced_plan.id)
            self.fields["coverage_plan"].initial = forced_plan
            self.fields["coverage_plan"].widget.attrs["disabled"] = True

    def clean_coverage_percent(self):
        value = self.cleaned_data.get("coverage_percent")
        if value is None:
            return value
        if value < 0 or value > 100:
            raise ValidationError("Le pourcentage doit être entre 0 et 100.")
        return value

    def clean(self):
        cleaned = super().clean()
        if self.forced_plan is not None:
            cleaned["coverage_plan"] = self.forced_plan
        plan = cleaned.get("coverage_plan")
        category = cleaned.get("category")
        if plan and category:
            qs = CoverageRule.objects.filter(coverage_plan=plan, category=category)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error("category", ValidationError("Une règle existe déjà pour cette formule et cette catégorie."))
        return cleaned


# ---------- PaymentMethod ----------

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ["name", "code", "method_type", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Ex: Virement bancaire"}),
            "code": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Ex: VIREMENT"}),
            "method_type": forms.Select(attrs={"class": "no-tom-select block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm"}),
            "is_active": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
        }


# ---------- Category ----------

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "is_pharmacy", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Nom de la catégorie"}),
            "is_pharmacy": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
            "is_active": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
        }


# ---------- User Management ----------

User = get_user_model()


class ProfileSelfEditForm(forms.Form):
    """Formulaire limité pour l'édition de son propre profil : nom, email, changement MDP (actuel + nouveau)."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Nom utilisateur"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": _INPUT_CLASS, "placeholder": "email@domaine.com"}),
    )
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS, "placeholder": "Mot de passe actuel (obligatoire pour changer)"}),
        label="Mot de passe actuel",
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS, "placeholder": "Laisser vide pour ne pas changer"}),
        label="Nouveau mot de passe",
    )
    new_password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS, "placeholder": "Confirmer le nouveau mot de passe"}),
        label="Confirmer le nouveau mot de passe",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["username"].initial = self.user.username
            self.fields["email"].initial = self.user.email or ""

    def clean_username(self):
        value = (self.cleaned_data.get("username") or "").strip()
        if not value:
            raise ValidationError("Le nom utilisateur est requis.")
        qs = User.objects.exclude(pk=self.user.pk) if self.user else User.objects.all()
        if qs.filter(username__iexact=value).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def clean(self):
        cleaned = super().clean()
        new_password = (cleaned.get("new_password") or "").strip()
        new_password_confirm = (cleaned.get("new_password_confirm") or "").strip()
        current_password = cleaned.get("current_password") or ""

        if new_password:
            if not current_password:
                self.add_error("current_password", ValidationError("Indiquez votre mot de passe actuel pour en définir un nouveau."))
            elif self.user and not self.user.check_password(current_password):
                self.add_error("current_password", ValidationError("Mot de passe actuel incorrect."))
            if new_password != new_password_confirm:
                self.add_error("new_password_confirm", ValidationError("Les deux nouveaux mots de passe ne correspondent pas."))
            if len(new_password) < 8:
                self.add_error("new_password", ValidationError("Le nouveau mot de passe doit contenir au moins 8 caractères."))
        elif new_password_confirm:
            self.add_error("new_password_confirm", ValidationError("Saisissez aussi le nouveau mot de passe."))

        return cleaned

    def save(self):
        self.user.username = self.cleaned_data["username"]
        self.user.email = self.cleaned_data.get("email") or ""
        new_password = (self.cleaned_data.get("new_password") or "").strip()
        if new_password:
            self.user.set_password(new_password)
        self.user.save()
        return self.user


class UserManagementForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS, "placeholder": "Laisser vide pour ne pas changer"}),
    )
    role = forms.ChoiceField(choices=UserRole.choices, widget=forms.Select(attrs={"class": "block w-full"}))
    hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.none(),  # set in __init__ by role
        required=False,
        empty_label="———",
        widget=forms.Select(attrs={"class": f"{_INPUT_CLASS} no-tom-select"}),
        label="Hôpital / Pharmacie",
    )
    ipm = forms.ModelChoiceField(
        queryset=IPM.objects.none(),  # set in __init__
        required=False,
        empty_label="———",
        widget=forms.Select(attrs={"class": f"{_INPUT_CLASS} no-tom-select"}),
        label="IPM",
    )

    class Meta:
        model = User
        fields = ["username", "email", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": _INPUT_CLASS, "placeholder": "Nom utilisateur"}),
            "email": forms.EmailInput(attrs={"class": _INPUT_CLASS, "placeholder": "email@domaine.com"}),
            "is_active": forms.CheckboxInput(attrs={"class": _CHECK_CLASS}),
        }

    def _effective_role(self):
        data = self.data if self.is_bound else None
        profile = getattr(self.instance, "staff_profile", None) if self.instance and self.instance.pk else None
        return (data.get("role") if data else None) or (profile.role if profile else UserRole.DOCTOR)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = None
        if self.instance and self.instance.pk:
            try:
                profile = self.instance.staff_profile
            except ObjectDoesNotExist:
                pass
        self.fields["role"].initial = profile.role if profile else UserRole.DOCTOR
        self.fields["hospital"].queryset = Hospital.objects.filter(is_active=True).order_by("name")
        self.fields["hospital"].label = "Hôpital / Pharmacie"
        self.fields["hospital"].initial = getattr(profile, "hospital_id", None)
        # Champ IPM : valeur initiale = instance (profile.ipm) pour affichage fiable à l'édition
        initial_ipm = None
        initial_ipm_id = None
        if profile:
            initial_ipm_id = getattr(profile, "ipm_id", None)
            if hasattr(profile, "ipm"):
                try:
                    initial_ipm = profile.ipm
                except ObjectDoesNotExist:
                    initial_ipm = None
        base_qs = IPM.objects.filter(is_active=True).order_by("name")
        if initial_ipm_id:
            # Toujours inclure l'IPM actuelle du profil dans les choix (même si inactive)
            self.fields["ipm"].queryset = IPM.objects.filter(
                Q(is_active=True) | Q(pk=initial_ipm_id)
            ).distinct().order_by("name")
        else:
            self.fields["ipm"].queryset = base_qs
        self.fields["ipm"].initial = initial_ipm if initial_ipm is not None else initial_ipm_id

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        ipm = cleaned.get("ipm")
        hospital = cleaned.get("hospital")
        password = cleaned.get("password")
        if role == UserRole.IPM_ADMIN and not ipm:
            self.add_error("ipm", ValidationError("L'IPM est requise pour un IPM Admin."))
        if role == UserRole.DOCTOR and hospital and hospital.establishment_type == EstablishmentType.PHARMACY:
            self.add_error("hospital", ValidationError("Sélectionnez un hôpital ou une clinique (pas une pharmacie)."))
        if role == UserRole.PHARMACY and hospital and hospital.establishment_type != EstablishmentType.PHARMACY:
            self.add_error("hospital", ValidationError("Sélectionnez une pharmacie."))
        if not self.instance.pk and not password:
            self.add_error("password", ValidationError("Le mot de passe est requis à la création."))
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            profile, _ = StaffProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data["role"]
            profile.hospital = self.cleaned_data.get("hospital")
            if hasattr(profile, "ipm"):
                profile.ipm = self.cleaned_data.get("ipm")
                if profile.ipm:
                    profile.ipm_name = profile.ipm.name  # legacy sync
                else:
                    profile.ipm_name = ""
            profile.save()
        return user


# ──────────────────────────────────────────────
# Notification (canaux : Email, SMS, WhatsApp)
# ──────────────────────────────────────────────

_INPUT_CLASS_NOTIF = "block w-full rounded-xl border border-slate-300 py-2.5 px-4 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm"


class NotificationChannelConfigForm(forms.Form):
    """Formulaire de configuration d'un canal (actif/inactif + paramètres selon le type)."""
    is_active = forms.BooleanField(required=False, initial=False, label="Activer ce canal")
    # Email
    email_host = forms.CharField(required=False, max_length=255, label="Serveur SMTP", widget=forms.TextInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "smtp.example.com"}))
    email_port = forms.IntegerField(required=False, min_value=1, max_value=65535, label="Port", widget=forms.NumberInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "587"}))
    email_use_tls = forms.BooleanField(required=False, initial=True, label="Utiliser TLS")
    email_user = forms.CharField(required=False, max_length=128, label="Utilisateur", widget=forms.TextInput(attrs={"class": _INPUT_CLASS_NOTIF, "autocomplete": "off"}))
    email_password = forms.CharField(required=False, max_length=128, label="Mot de passe", widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS_NOTIF, "autocomplete": "new-password"}))
    email_from = forms.EmailField(required=False, label="Adresse expéditeur", widget=forms.EmailInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "noreply@example.com"}))
    # SMS
    sms_api_url = forms.URLField(required=False, label="URL API SMS", widget=forms.URLInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "https://api.sms.pro/send"}))
    sms_api_key = forms.CharField(required=False, max_length=255, label="Clé API", widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS_NOTIF, "autocomplete": "off"}))
    sms_sender = forms.CharField(required=False, max_length=20, label="Expéditeur (nom court)", widget=forms.TextInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "REMEDY"}))
    # WhatsApp (optionnel, champs similaires)
    whatsapp_api_url = forms.URLField(required=False, label="URL API WhatsApp", widget=forms.URLInput(attrs={"class": _INPUT_CLASS_NOTIF}))
    whatsapp_api_key = forms.CharField(required=False, max_length=255, label="Clé API", widget=forms.PasswordInput(attrs={"class": _INPUT_CLASS_NOTIF, "autocomplete": "off"}))

    # Modèles de message (contenu envoyé au destinataire)
    message_subject = forms.CharField(
        required=False,
        max_length=255,
        label="Sujet du message (email)",
        widget=forms.TextInput(attrs={"class": _INPUT_CLASS_NOTIF, "placeholder": "Votre réclamation — à valider"}),
    )
    message_body = forms.CharField(
        required=False,
        label="Texte du message",
        widget=forms.Textarea(attrs={"class": _INPUT_CLASS_NOTIF + " min-h-[180px]", "rows": 8, "placeholder": "Bonjour {{ patient_name }} !\n\nJ'espère que vous allez bien. Pour valider votre réclamation, cliquez ici : {{ verify_link }}\n\nÀ bientôt, l'équipe REMEDY"}),
    )

    def __init__(self, channel, config_instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = channel
        self.config_instance = config_instance
        if config_instance:
            self.fields["is_active"].initial = config_instance.is_active
            cfg = config_instance.config or {}
            if channel == NotificationChannel.EMAIL:
                self.fields["email_host"].initial = cfg.get("host", "")
                self.fields["email_port"].initial = cfg.get("port") or 587
                self.fields["email_use_tls"].initial = cfg.get("use_tls", True)
                self.fields["email_user"].initial = cfg.get("user", "")
                self.fields["email_from"].initial = cfg.get("from_email", "")
            elif channel == NotificationChannel.SMS:
                self.fields["sms_api_url"].initial = cfg.get("api_url", "")
                self.fields["sms_api_key"].initial = cfg.get("api_key", "")
                self.fields["sms_sender"].initial = cfg.get("sender", "")
            elif channel == NotificationChannel.WHATSAPP:
                self.fields["whatsapp_api_url"].initial = cfg.get("api_url", "")
                self.fields["whatsapp_api_key"].initial = cfg.get("api_key", "")
            # Modèles de message (tous canaux)
            self.fields["message_subject"].initial = cfg.get("subject_template", "")
            self.fields["message_body"].initial = cfg.get("body_template", "")
        else:
            # Valeurs par défaut pour une nouvelle config
            _default_body = (
                "Bonjour {{ patient_name }} !\n\n"
                "J'espère que vous allez bien. Nous vous envoyons ce message concernant votre réclamation santé.\n\n"
                "Pour valider votre dossier, cliquez sur le lien suivant : {{ verify_link }}\n\n"
                "À bientôt,\nL'équipe REMEDY"
            )
            if self.channel == NotificationChannel.EMAIL:
                self.fields["message_subject"].initial = "Votre réclamation REMEDY — à valider"
            self.fields["message_body"].initial = _default_body

    def get_config_dict(self):
        """Construit le dict config à sauvegarder selon le canal."""
        if self.channel == NotificationChannel.EMAIL:
            cfg = {
                "host": (self.cleaned_data.get("email_host") or "").strip() or None,
                "port": self.cleaned_data.get("email_port") or 587,
                "use_tls": self.cleaned_data.get("email_use_tls", True),
                "user": (self.cleaned_data.get("email_user") or "").strip() or None,
                "password": (self.cleaned_data.get("email_password") or "").strip() or None,
                "from_email": (self.cleaned_data.get("email_from") or "").strip() or None,
            }
        elif self.channel == NotificationChannel.SMS:
            cfg = {
                "api_url": (self.cleaned_data.get("sms_api_url") or "").strip() or None,
                "api_key": (self.cleaned_data.get("sms_api_key") or "").strip() or None,
                "sender": (self.cleaned_data.get("sms_sender") or "").strip() or None,
            }
        elif self.channel == NotificationChannel.WHATSAPP:
            cfg = {
                "api_url": (self.cleaned_data.get("whatsapp_api_url") or "").strip() or None,
                "api_key": (self.cleaned_data.get("whatsapp_api_key") or "").strip() or None,
            }
        else:
            cfg = {}
        # Modèles de message (tous canaux)
        subject = (self.cleaned_data.get("message_subject") or "").strip()
        body = (self.cleaned_data.get("message_body") or "").strip()
        if subject:
            cfg["subject_template"] = subject
        if body:
            cfg["body_template"] = body
        return cfg

    def save(self):
        if not self.config_instance:
            self.config_instance = NotificationChannelConfig(channel=self.channel)
        self.config_instance.is_active = self.cleaned_data.get("is_active", False)
        cfg = self.get_config_dict()
        old = self.config_instance.config or {}
        if self.channel == NotificationChannel.EMAIL:
            if not (self.cleaned_data.get("email_password") or "").strip():
                cfg["password"] = old.get("password")
        elif self.channel == NotificationChannel.SMS and not (self.cleaned_data.get("sms_api_key") or "").strip():
            cfg["api_key"] = old.get("api_key")
        elif self.channel == NotificationChannel.WHATSAPP and not (self.cleaned_data.get("whatsapp_api_key") or "").strip():
            cfg["api_key"] = old.get("api_key")
        self.config_instance.config = cfg
        self.config_instance.save()
        return self.config_instance
