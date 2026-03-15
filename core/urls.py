from django.urls import path

from .views import (
    demo_request_submit,
    home,
    ipm_dashboard,
    landing_page,
    provider_dashboard,
    superadmin_dashboard,
    superadmin_demo_notification_config,
    superadmin_demo_request_detail,
    superadmin_demo_request_list,
    superadmin_email_log_detail,
    superadmin_email_log_list,
    superadmin_email_log_resend,
    superadmin_testimonial_add,
    superadmin_testimonial_delete,
    superadmin_testimonial_edit,
    superadmin_testimonial_list,
)

urlpatterns = [
    path("", home, name="home"),
    path("landing/", landing_page, name="landing"),
    path("demo/request/", demo_request_submit, name="demo_request_submit"),
    path("superadmin/", superadmin_dashboard, name="superadmin_dashboard"),
    path("superadmin/avis/", superadmin_testimonial_list, name="superadmin_testimonial_list"),
    path("superadmin/avis/ajouter/", superadmin_testimonial_add, name="superadmin_testimonial_add"),
    path("superadmin/avis/<int:pk>/", superadmin_testimonial_edit, name="superadmin_testimonial_edit"),
    path("superadmin/avis/<int:pk>/supprimer/", superadmin_testimonial_delete, name="superadmin_testimonial_delete"),
    path("superadmin/mails-demandes/", superadmin_demo_notification_config, name="superadmin_demo_notification_config"),
    path("superadmin/demandes-demo/", superadmin_demo_request_list, name="superadmin_demo_request_list"),
    path("superadmin/demandes-demo/<int:pk>/", superadmin_demo_request_detail, name="superadmin_demo_request_detail"),
    path("superadmin/emails/", superadmin_email_log_list, name="superadmin_email_log_list"),
    path("superadmin/emails/<int:pk>/", superadmin_email_log_detail, name="superadmin_email_log_detail"),
    path("superadmin/emails/<int:pk>/resend/", superadmin_email_log_resend, name="superadmin_email_log_resend"),
    path("dashboard/ipm/", ipm_dashboard, name="ipm_dashboard"),
    path("dashboard/provider/", provider_dashboard, name="provider_dashboard"),
]
