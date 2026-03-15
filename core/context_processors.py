from django.core.exceptions import ObjectDoesNotExist

from accounts.models import UserRole
from accounts.roles import get_user_role


def remedy_user_role(request):
    """Expose user role and (for IPM Admin) their IPM, (for Doctor/Pharmacy) their hospital. Never raise."""
    role = None
    role_label = None
    my_ipm = None
    my_hospital = None
    try:
        if getattr(request, "user", None) and getattr(request.user, "is_authenticated", False):
            role = get_user_role(request.user)
            role_label = dict(UserRole.choices).get(role, role) if role else "User"
            try:
                profile = request.user.staff_profile
            except ObjectDoesNotExist:
                profile = None
            if role == "IPM_ADMIN":
                try:
                    if profile and getattr(profile, "ipm_id", None):
                        my_ipm = getattr(profile, "ipm", None)
                        if my_ipm is None and profile:
                            ipm_name = (getattr(profile, "ipm_name", None) or "").strip()
                            if ipm_name:
                                from claims.models import IPM
                                my_ipm = IPM.objects.filter(name__iexact=ipm_name).first()
                    elif profile:
                        ipm_name = (getattr(profile, "ipm_name", None) or "").strip()
                        if ipm_name:
                            from claims.models import IPM
                            my_ipm = IPM.objects.filter(name__iexact=ipm_name).first()
                except (AttributeError, ObjectDoesNotExist):
                    pass
            elif role in ("DOCTOR", "PHARMACY") and profile and getattr(profile, "hospital_id", None):
                try:
                    my_hospital = getattr(profile, "hospital", None)
                except (AttributeError, ObjectDoesNotExist):
                    pass
    except Exception:
        pass
    return {
        "remedy_user_role": role,
        "remedy_user_role_label": role_label,
        "remedy_my_ipm": my_ipm,
        "remedy_my_hospital": my_hospital,
    }