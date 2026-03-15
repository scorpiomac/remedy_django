from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StaffProfile, UserRole

User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.is_superuser:
        role = UserRole.SYSTEM_ADMIN
    else:
        role = UserRole.DOCTOR
    StaffProfile.objects.create(user=instance, role=role)
