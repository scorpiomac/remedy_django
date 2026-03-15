from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import RemedyLoginForm
from .models import UserRole
from .roles import get_user_role


@login_not_required
class RemedyLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = RemedyLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        role = get_user_role(self.request.user)
        if role == UserRole.SYSTEM_ADMIN:
            return reverse_lazy("superadmin_dashboard")
        if role == UserRole.IPM_ADMIN:
            return reverse_lazy("ipm_dashboard")
        return reverse_lazy("provider_dashboard")


class RemedyLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]
    next_page = reverse_lazy("login")
