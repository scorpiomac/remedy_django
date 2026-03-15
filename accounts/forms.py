from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class RemedyLoginForm(AuthenticationForm):
    """Formulaire de connexion acceptant identifiant = username OU email."""

    username = forms.CharField(
        label="Utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-xl border border-slate-300 py-2.5 pl-10 pr-3 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                "placeholder": "Nom d'utilisateur ou email",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-xl border border-slate-300 py-2.5 pl-10 pr-3 text-slate-900 shadow-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 sm:text-sm",
                "placeholder": "Votre mot de passe",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean(self):
        login = (self.cleaned_data.get("username") or "").strip()
        password = self.cleaned_data.get("password")

        if not login or not password:
            return self.cleaned_data

        # Si ça ressemble à un email, chercher l'utilisateur par email
        if "@" in login:
            user = User.objects.filter(email__iexact=login).first()
            if user:
                login = user.username
            # sinon on garde login tel quel (authenticate échouera)

        user = authenticate(self.request, username=login, password=password)
        if user is None:
            raise forms.ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
            )
        self.confirm_login_allowed(user)
        self.user_cache = user
        return self.cleaned_data
