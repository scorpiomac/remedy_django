import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

from accounts.models import UserRole
from accounts.roles import get_user_role
from core.forms import DemoRequestBackofficeForm, DemoRequestForm, DemoRequestNotificationConfigForm, TestimonialForm
from core.models import DemoRequest, DemoRequestNotificationConfig, EmailLog, Testimonial

logger = logging.getLogger(__name__)
from claims.models import Claim, ClaimStatus, CoveragePlan, CoverageRule, IPM, Patient
from claims.views import _ipm_scope_queryset

STATUS_LABELS = dict(ClaimStatus.choices)


def _claim_to_dict(claim):
    plan = getattr(claim.patient, "coverage_plan", None)
    return {
        "id": claim.id,
        "patient": claim.patient.full_name,
        "ipm": getattr(claim.patient.ipm, "name", "") if hasattr(claim.patient, "ipm") else "",
        "formule": plan.name if plan else "",
        "category": claim.category.name,
        "provider": claim.provider.username,
        "total_amount": str(claim.total_amount),
        "status": claim.status,
        "status_display": claim.get_status_display(),
        "created_at": claim.created_at.strftime("%d/%m/%Y"),
        "detail_url": reverse("claim_detail", args=[claim.id]),
    }


def robots_txt(request):
    """Réponse robots.txt pour le référencement."""
    base = request.build_absolute_uri("/")
    sitemap_url = request.build_absolute_uri(reverse("sitemap_xml"))
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /accounts/login/\n"
        "Disallow: /superadmin/\n"
        "Disallow: /dashboard/\n"
        "Disallow: /claims/\n"
        "\n"
        f"Sitemap: {sitemap_url}\n"
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """Sitemap XML des pages publiques (landing, connexion)."""
    base = request.build_absolute_uri("/").rstrip("/")
    lastmod = timezone.now().strftime("%Y-%m-%d")
    urls = [
        (base + "/", "1.0", "weekly"),
        (base + reverse("landing"), "0.9", "monthly"),
        (base + reverse("login"), "0.5", "monthly"),
    ]
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, changefreq in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <changefreq>{changefreq}</changefreq>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")
    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")


def _get_landing_context(request):
    """Contexte commun pour le rendu de la landing."""
    canonical_url = request.build_absolute_uri("/")
    share_image_url = None
    try:
        from pathlib import Path
        og_path = Path(settings.STATIC_ROOT) / "img" / "og-landing.png"
        if og_path.exists():
            share_image_url = request.build_absolute_uri(static("img/og-landing.png"))
    except Exception:
        pass
    dashboard_image = None
    try:
        from pathlib import Path
        dash_path = Path(settings.STATIC_ROOT) / "img" / "remedi-dashboard-ipm.png"
        if dash_path.exists():
            dashboard_image = request.build_absolute_uri(static("img/remedi-dashboard-ipm.png"))
    except Exception:
        pass
    logo_url = request.build_absolute_uri(static("img/remedi-logo-banner.png"))
    testimonials = list(Testimonial.objects.filter(is_active=True).order_by("order", "created_at")[:10])
    return {
        "canonical_url": canonical_url,
        "share_image_url": share_image_url,
        "dashboard_image": dashboard_image,
        "sitemap_url": request.build_absolute_uri(reverse("sitemap_xml")),
        "site_name": "Remedi",
        "logo_url": logo_url,
        "testimonials": testimonials,
    }


def _send_demo_notification_email(request, demo_request):
    """Envoie les emails de notification (équipe + optionnellement copie client) avec templates HTML et log."""
    from django.template.loader import render_to_string

    from core.mail_utils import send_and_log_email

    if not getattr(settings, "EMAIL_HOST", None) or not getattr(settings, "EMAIL_HOST_USER", None):
        logger.warning("Email non configuré (REMEDY_EMAIL_HOST / REMEDY_EMAIL_HOST_USER), notification démo non envoyée.")
        return

    config = DemoRequestNotificationConfig.objects.first()
    site_name = getattr(settings, "SITE_NAME", "Remedi")
    admin_url = request.build_absolute_uri(reverse("admin:core_demorequest_change", args=[demo_request.pk])) if request else ""

    # Destinataires équipe : config en priorité, sinon variable d'environnement
    to_emails = []
    if config:
        to_emails = config.get_recipient_list()
    if not to_emails:
        to_emails = getattr(settings, "REMEDY_DEMO_NOTIFICATION_EMAILS", None) or []

    ctx = {"demo_request": demo_request, "site_name": site_name, "admin_url": admin_url}
    related_ref = f"demorequest:{demo_request.pk}"

    # Email à l'équipe (HTML + fallback texte)
    if to_emails:
        subject = f"[Remedi] Nouvelle demande de démo – {demo_request.organisation}"
        body_plain = (
            f"Une nouvelle demande de démo a été enregistrée.\n\n"
            f"Prénom : {demo_request.first_name}\nNom : {demo_request.last_name}\n"
            f"Email : {demo_request.email}\nTéléphone : {demo_request.phone or '—'}\n"
            f"Organisation : {demo_request.organisation}\nProfil : {demo_request.get_profile_display()}\n\n"
            f"Message :\n{demo_request.message or '—'}\n\n"
            f"Admin : {admin_url}"
        )
        html_body = render_to_string("core/email/demo_notification_team.html", ctx)
        send_and_log_email(
            to_list=to_emails,
            subject=subject,
            body_plain=body_plain,
            body_html=html_body,
            email_type="demo_team",
            related_ref=related_ref,
        )

    # Copie client (confirmation) si activée dans la config
    if config and config.send_copy_to_client and demo_request.email:
        subject_client = "Votre demande de démo Remedi a bien été reçue"
        body_plain_client = (
            f"Bonjour {demo_request.first_name},\n\n"
            f"Nous avons bien reçu votre demande de démo pour {demo_request.organisation}.\n"
            "Notre équipe vous recontactera très prochainement.\n\n"
            "Remedi – contact@remediafrica.com"
        )
        html_client = render_to_string("core/email/demo_notification_client.html", ctx)
        send_and_log_email(
            to_list=[demo_request.email],
            subject=subject_client,
            body_plain=body_plain_client,
            body_html=html_client,
            email_type="demo_client",
            related_ref=related_ref,
        )


def demo_request_submit(request):
    """Enregistre une demande de démo depuis la landing et redirige avec message."""
    if request.method != "POST":
        return redirect("home")
    form = DemoRequestForm(request.POST)
    if not form.is_valid():
        context = _get_landing_context(request)
        context["demo_submitted"] = request.POST
        context["demo_errors"] = form.errors
        return render(request, "core/landing.html", context)
    try:
        demo_request = form.save(commit=False)
        demo_request.status = "new"
        demo_request.save()
    except Exception as e:
        logger.exception("Enregistrement demande de démo échoué : %s", e)
        messages.error(
            request,
            "Une erreur technique s’est produite. Veuillez réessayer ou nous contacter à contact@remediafrica.com.",
        )
        context = _get_landing_context(request)
        context["demo_submitted"] = request.POST
        context["demo_errors"] = {}
        return render(request, "core/landing.html", context)
    try:
        _send_demo_notification_email(request, demo_request)
    except Exception:
        pass  # déjà loggé dans _send_demo_notification_email
    messages.success(
        request,
        "Merci ! Votre demande de démo a bien été enregistrée. Nous vous recontacterons rapidement.",
    )
    return redirect("landing")


def landing_page(request):
    """Page d'accueil publique (landing) pour les visiteurs non connectés."""
    return render(request, "core/landing.html", _get_landing_context(request))


def home(request):
    if not getattr(request.user, "is_authenticated", False):
        return landing_page(request)
    try:
        role = get_user_role(request.user)
        if role == UserRole.SYSTEM_ADMIN:
            return superadmin_dashboard(request)
        if role == UserRole.IPM_ADMIN:
            return ipm_dashboard(request)
        return provider_dashboard(request)
    except Exception as exc:
        logger.exception("home view error: %s", exc)
        return redirect("login")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_dashboard(request):
    recent = list(
        Claim.objects.select_related("patient", "provider", "patient__ipm", "patient__coverage_plan")
        .order_by("-created_at")[:50]
    )
    context = {
        "total_ipms": IPM.objects.count(),
        "total_patients": Patient.objects.count(),
        "total_claims": Claim.objects.count(),
        "submitted_claims": Claim.objects.filter(status=ClaimStatus.SUBMITTED).count(),
        "blocked_claims": Claim.objects.filter(status=ClaimStatus.BLOCKED).count(),
        "coverage_rules": CoverageRule.objects.filter(is_active=True).count(),
        "total_plans": CoveragePlan.objects.filter(is_active=True).count(),
        "recent_claims": recent,
        "claims_data": [_claim_to_dict(c) for c in recent],
    }
    return render(request, "core/superadmin_dashboard.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_testimonial_list(request):
    """Liste des avis / témoignages (backoffice Remedi)."""
    testimonials = Testimonial.objects.all().order_by("order", "created_at")
    form = TestimonialForm()
    return render(
        request,
        "core/superadmin_testimonials.html",
        {"testimonials": testimonials, "form": form},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_testimonial_add(request):
    """Ajout d'un avis depuis le backoffice."""
    if request.method != "POST":
        return redirect("superadmin_testimonial_list")
    form = TestimonialForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "L'avis a été ajouté.")
    else:
        messages.error(request, "Vérifiez les champs du formulaire.")
        testimonials = Testimonial.objects.all().order_by("order", "created_at")
        return render(request, "core/superadmin_testimonials.html", {"testimonials": testimonials, "form": form})
    return redirect("superadmin_testimonial_list")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_testimonial_edit(request, pk):
    """Modification d'un avis (backoffice)."""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "L'avis a été enregistré.")
            return redirect("superadmin_testimonial_list")
    else:
        form = TestimonialForm(instance=testimonial)
    testimonials = Testimonial.objects.all().order_by("order", "created_at")
    return render(
        request,
        "core/superadmin_testimonials.html",
        {"testimonials": testimonials, "form": form, "editing": testimonial},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_testimonial_delete(request, pk):
    """Suppression d'un avis (backoffice)."""
    if request.method != "POST":
        return redirect("superadmin_testimonial_list")
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, "L'avis a été supprimé.")
    return redirect("superadmin_testimonial_list")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_demo_notification_config(request):
    """Configuration : qui reçoit les mails de demande de démo (backoffice Remedi)."""
    config, _ = DemoRequestNotificationConfig.objects.get_or_create(
        defaults={"notification_emails": "", "send_copy_to_client": False}
    )
    if request.method == "POST":
        form = DemoRequestNotificationConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "La configuration des mails de démo a été enregistrée.")
            return redirect("superadmin_demo_notification_config")
    else:
        form = DemoRequestNotificationConfigForm(instance=config)
    return render(
        request,
        "core/superadmin_demo_notification_config.html",
        {"form": form, "config": config},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_demo_request_list(request):
    """Liste des demandes de démo (backoffice Remedi)."""
    qs = DemoRequest.objects.all().order_by("-created_at")
    status_filter = request.GET.get("status", "").strip()
    if status_filter and status_filter in dict(DemoRequest.STATUS_CHOICES):
        qs = qs.filter(status=status_filter)
    return render(
        request,
        "core/superadmin_demo_requests.html",
        {"demo_requests": qs, "status_filter": status_filter},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_email_log_list(request):
    """Liste des emails envoyés par le système (backoffice Remedi)."""
    qs = EmailLog.objects.all().order_by("-sent_at")
    status_filter = request.GET.get("status", "").strip()
    if status_filter in ("sent", "failed"):
        qs = qs.filter(status=status_filter)
    type_filter = request.GET.get("type", "").strip()
    if type_filter:
        qs = qs.filter(email_type=type_filter)
    return render(
        request,
        "core/superadmin_email_log_list.html",
        {"email_logs": qs, "status_filter": status_filter, "type_filter": type_filter},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_email_log_detail(request, pk):
    """Détail d'un log email (backoffice)."""
    email_log = get_object_or_404(EmailLog, pk=pk)
    return render(request, "core/superadmin_email_log_detail.html", {"email_log": email_log})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_email_log_resend(request, pk):
    """Renvoie un email à partir d'un log (backoffice)."""
    if request.method != "POST":
        return redirect("superadmin_email_log_list")
    email_log = get_object_or_404(EmailLog, pk=pk)
    from core.mail_utils import resend_email

    new_log = resend_email(email_log)
    if new_log and new_log.status == "sent":
        messages.success(request, "Email renvoyé avec succès.")
        return redirect("superadmin_email_log_detail", pk=new_log.pk)
    err = (new_log.error_message if new_log and getattr(new_log, "error_message", None) else "") or "Destinataires invalides ou erreur inconnue."
    messages.error(request, f"Échec du renvoi : {err}")
    return redirect("superadmin_email_log_detail", pk=pk)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def superadmin_demo_request_detail(request, pk):
    """Détail d'une demande de démo et mise à jour du statut / notes (backoffice)."""
    demo_request = get_object_or_404(DemoRequest, pk=pk)
    if request.method == "POST":
        form = DemoRequestBackofficeForm(request.POST, instance=demo_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Demande de démo mise à jour.")
            return redirect("superadmin_demo_request_detail", pk=pk)
    else:
        form = DemoRequestBackofficeForm(instance=demo_request)
    return render(
        request,
        "core/superadmin_demo_request_detail.html",
        {"demo_request": demo_request, "form": form},
    )


@login_required
def ipm_dashboard(request):
    try:
        profile = request.user.staff_profile
    except ObjectDoesNotExist:
        profile = None
    if not profile or profile.role != UserRole.IPM_ADMIN:
        return HttpResponseForbidden("Access denied.")

    scope = _ipm_scope_queryset(request.user)
    ipm = getattr(profile, "ipm", None)
    ipm_name = ipm.name if ipm else (getattr(profile, "ipm_name", "") or "").strip() or "Mon IPM"
    scoped_claims = Claim.objects.select_related(
        "patient", "provider", "patient__ipm", "category", "patient__coverage_plan"
    ).filter(patient__ipm__in=scope)
    _breakdown = scoped_claims.values("status").annotate(total=Count("id")).order_by("status")
    status_breakdown = [
        {"status": s["status"], "status_display": STATUS_LABELS.get(s["status"], s["status"]), "total": s["total"]}
        for s in _breakdown
    ]

    recent = list(scoped_claims.order_by("-created_at")[:50])
    context = {
        "ipm_name": ipm_name or "Mon IPM",
        "total_patients": Patient.objects.filter(ipm__in=scope).count(),
        "total_claims": scoped_claims.count(),
        "submitted_claims": scoped_claims.filter(status=ClaimStatus.SUBMITTED).count(),
        "blocked_claims": scoped_claims.filter(status=ClaimStatus.BLOCKED).count(),
        "recent_claims": recent,
        "claims_data": [_claim_to_dict(c) for c in recent],
        "status_breakdown": status_breakdown,
    }
    return render(request, "core/ipm_dashboard.html", context)


@login_required
def provider_dashboard(request):
    if request.user.is_superuser:
        return superadmin_dashboard(request)

    claims_qs = Claim.objects.select_related(
        "patient", "category", "patient__ipm", "patient__coverage_plan"
    ).filter(provider=request.user).order_by("-created_at")
    recent = list(claims_qs[:50])
    context = {
        "total_claims": claims_qs.count(),
        "draft_claims": claims_qs.filter(status=ClaimStatus.DRAFT).count(),
        "submitted_claims": claims_qs.filter(status=ClaimStatus.SUBMITTED).count(),
        "blocked_claims": claims_qs.filter(status=ClaimStatus.BLOCKED).count(),
        "recent_claims": recent,
        "claims_data": [_claim_to_dict(c) for c in recent],
    }
    return render(request, "core/provider_dashboard.html", context)
