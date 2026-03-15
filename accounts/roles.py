from django.core.exceptions import ObjectDoesNotExist

from .models import UserRole


def get_user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserRole.SYSTEM_ADMIN
    try:
        profile = user.staff_profile
    except ObjectDoesNotExist:
        profile = None
    if profile:
        return profile.role
    return UserRole.DOCTOR


def is_provider(user):
    return get_user_role(user) in {UserRole.DOCTOR, UserRole.PHARMACY}


def is_ipm_admin(user):
    return get_user_role(user) == UserRole.IPM_ADMIN
