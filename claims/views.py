from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, login_not_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from accounts.models import StaffProfile, UserRole
from accounts.roles import get_user_role, is_ipm_admin, is_provider

from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from .forms import (
    ClaimCreateForm,
    ClaimDocumentUploadForm,
    ClaimEditForm,
    CategoryForm,
    CoveragePlanForm,
    CoverageRuleForm,
    HospitalForm,
    IPMForm,
    NotificationChannelConfigForm,
    PatientForm,
    PaymentMethodForm,
    ProfileSelfEditForm,
    UserManagementForm,
)
from .models import (
    Category,
    Claim,
    ClaimAuditLog,
    ClaimDocument,
    ClaimStatus,
    CoveragePlan,
    CoverageRule,
    DocumentType,
    EstablishmentPaymentOption,
    EstablishmentType,
    Hospital,
    IPM,
    IPMPaymentOption,
    NotificationChannel,
    NotificationChannelConfig,
    NotificationLog,
    Patient,
    PaymentMethod,
)
from .notification_service import send_claim_notifications
from .state_machine import ClaimStateMachine, ClaimTransitionError

User = get_user_model()


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _can_access_claim(user, claim):
    """Peut voir le dossier (lecture)."""
    if user.is_superuser or claim.provider_id == user.id:
        return True
    if is_ipm_admin(user):
        try:
            profile = user.staff_profile
        except ObjectDoesNotExist:
            return False
        ipm_id = getattr(profile, "ipm_id", None)
        if ipm_id is not None:
            return claim.patient.ipm_id == ipm_id
        ipm_name = (getattr(profile, "ipm_name", "") or "").strip()
        if ipm_name and hasattr(claim.patient, "ipm") and claim.patient.ipm:
            return claim.patient.ipm.name == ipm_name
    return False


def _can_edit_claim(user, claim):
    """Peut modifier/supprimer le dossier (propriétaire ou superadmin uniquement)."""
    return user.is_superuser or claim.provider_id == user.id


def _audit(claim, actor, event, notes=""):
    ClaimAuditLog.objects.create(claim=claim, actor=actor, event=event, notes=notes)


def _claim_to_dict(claim):
    plan = getattr(claim.patient, "coverage_plan", None)
    return {
        "id": claim.id,
        "patient": claim.patient.full_name,
        "member_number": claim.patient.member_number,
        "ipm": claim.patient.ipm.name,
        "formule": plan.name if plan else "",
        "category": claim.category.name,
        "provider": claim.provider.username,
        "total_amount": str(claim.total_amount),
        "status": claim.status,
        "status_display": claim.get_status_display(),
        "updated_at": claim.updated_at.strftime("%d/%m/%Y %H:%M"),
        "detail_url": reverse("claim_detail", args=[claim.id]),
    }


def _can_manage_master_data(user):
    return user.is_superuser or is_ipm_admin(user)


def _ipm_scope_queryset(user):
    """Retourne le queryset des IPM accessibles par l'utilisateur. Superadmin = toutes ; sinon = l'IPM liée au profil (FK profile.ipm)."""
    if user.is_superuser:
        return IPM.objects.all()
    try:
        profile = user.staff_profile
    except ObjectDoesNotExist:
        return IPM.objects.none()
    # Lien par ForeignKey : profile.ipm
    ipm_id = getattr(profile, "ipm_id", None)
    if ipm_id is not None:
        return IPM.objects.filter(pk=ipm_id)
    # Fallback legacy : ipm_name (texte)
    ipm_name = (getattr(profile, "ipm_name", None) or "").strip()
    if not ipm_name:
        return IPM.objects.none()
    return IPM.objects.filter(name__iexact=ipm_name)


def _plan_scope_queryset(user):
    """Return CoveragePlan queryset scoped to user's IPM access."""
    ipms = _ipm_scope_queryset(user)
    return CoveragePlan.objects.filter(ipm__in=ipms).select_related("ipm")


def _superadmin_only(user):
    return user.is_superuser


def _build_category_rule_state(categories, request_post=None, existing_rules=None):
    """
    Build per-category state used by the formula wizard UI.
    """
    existing_rules = existing_rules or {}
    rows = []
    for category in categories:
        if request_post is not None:
            enabled = request_post.get(f"cat_enabled_{category.id}") == "on"
            percent = (request_post.get(f"cat_percent_{category.id}") or "").strip()
        else:
            rule = existing_rules.get(category.id)
            enabled = bool(rule and rule.is_active)
            percent = str(rule.coverage_percent) if enabled and rule else ""
        rows.append(
            {
                "id": category.id,
                "name": category.name,
                "is_pharmacy": category.is_pharmacy,
                "enabled": enabled,
                "percent": percent,
            }
        )
    return rows


def _extract_plan_rule_payload(request, categories):
    """
    Extract and validate selected categories + percentages from formula wizard.
    Returns: (payload_dict[category_id -> Decimal], errors[list[str]])
    """
    payload = {}
    errors = []
    for category in categories:
        enabled = request.POST.get(f"cat_enabled_{category.id}") == "on"
        raw_percent = (request.POST.get(f"cat_percent_{category.id}") or "").strip()
        if not enabled and not raw_percent:
            continue
        if not enabled and raw_percent:
            errors.append(f"Cochez la catégorie '{category.name}' pour appliquer le pourcentage saisi.")
            continue
        if enabled and not raw_percent:
            errors.append(f"Veuillez saisir un pourcentage pour '{category.name}'.")
            continue
        try:
            value = Decimal(raw_percent)
        except (InvalidOperation, ValueError):
            errors.append(f"Pourcentage invalide pour '{category.name}'.")
            continue
        if value < 0 or value > 100:
            errors.append(f"Le pourcentage de '{category.name}' doit être entre 0 et 100.")
            continue
        payload[category.id] = value
    return payload, errors


# ──────────────────────────────────────────────
# Claims
# ──────────────────────────────────────────────

@login_required
def claim_list(request):
    claims = Claim.objects.select_related(
        "patient", "category", "provider", "patient__ipm", "patient__coverage_plan"
    ).order_by("-created_at")
    if is_provider(request.user):
        claims = claims.filter(provider=request.user)
    elif is_ipm_admin(request.user):
        scope = _ipm_scope_queryset(request.user)
        if scope.exists():
            claims = claims.filter(patient__ipm__in=scope)

    status = request.GET.get("status", "").strip()
    if status:
        claims = claims.filter(status=status)

    query = request.GET.get("q", "").strip()
    if query:
        claims = claims.filter(patient__full_name__icontains=query)

    claims_list = list(claims[:500])
    return render(
        request,
        "claims/list.html",
        {
            "claims": claims_list,
            "claims_data": [_claim_to_dict(c) for c in claims_list],
            "status": status,
            "query": query,
            "status_choices": ClaimStatus.choices,
        },
    )


@login_required
def claim_create(request):
    if not is_provider(request.user) and not request.user.is_superuser:
        return HttpResponseForbidden("Only providers and superadmin can create claims.")

    form = ClaimCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            claim = form.save(commit=False)
            claim.provider = request.user
            claim.status = ClaimStatus.DRAFT
            claim.save()
            _audit(claim, request.user, "CLAIM_CREATED", "Draft created")
            docs_added = 0
            for i in range(20):
                f = request.FILES.get(f"document_file_{i}")
                if f:
                    doc_type = request.POST.get(f"document_type_{i}", "AUTRE")
                    ClaimDocument.objects.create(
                        claim=claim,
                        file=f,
                        original_name=f.name,
                        document_type=doc_type,
                    )
                    _audit(claim, request.user, "DOCUMENTS_UPLOADED", f"{f.name}")
                    docs_added += 1

            action = request.POST.get("action", "draft")
            if action == "create_and_submit" and docs_added:
                try:
                    ClaimStateMachine.submit(claim, request.user)
                    send_claim_notifications(claim, request)
                    messages.success(request, "Dossier créé et soumis avec succès.")
                except ClaimTransitionError as exc:
                    messages.warning(request, str(exc))
            elif action == "create_and_submit" and not docs_added:
                messages.warning(
                    request,
                    "Brouillon créé. Au moins un document est requis pour soumettre. Uploadez-le depuis la fiche détail.",
                )
            else:
                messages.success(request, "Brouillon créé avec succès.")
            return redirect("claim_detail", claim_id=claim.id)

    patients = Patient.objects.select_related("ipm", "coverage_plan").order_by("full_name")
    patients_summary = {}
    for p in patients:
        patients_summary[p.id] = {
            "member_number": p.member_number,
            "ipm_name": p.ipm.name,
            "formule": p.coverage_plan.name if p.coverage_plan else "",
        }

    return render(
        request,
        "claims/create.html",
        {
            "form": form,
            "document_type_choices": DocumentType.choices,
            "patients_summary": patients_summary,
        },
    )


@login_required
def claim_edit(request, claim_id):
    claim = get_object_or_404(Claim.objects.select_related("provider"), id=claim_id)
    if not _can_edit_claim(request.user, claim):
        return HttpResponseForbidden("Access denied.")
    if claim.status != ClaimStatus.DRAFT:
        messages.warning(request, "Seul un brouillon peut etre modifie.")
        return redirect("claim_detail", claim_id=claim.id)

    form = ClaimEditForm(request.POST or None, instance=claim)
    if request.method == "POST" and form.is_valid():
        form.save()
        _audit(claim, request.user, "CLAIM_EDITED", "Draft updated")
        messages.success(request, "Brouillon mis a jour.")
        return redirect("claim_detail", claim_id=claim.id)
    return render(request, "claims/edit.html", {"form": form, "claim": claim})


@login_required
def claim_delete(request, claim_id):
    claim = get_object_or_404(Claim.objects.select_related("provider"), id=claim_id)
    if not _can_edit_claim(request.user, claim):
        return HttpResponseForbidden("Access denied.")
    if claim.status != ClaimStatus.DRAFT:
        messages.warning(request, "Seul un brouillon peut etre supprime.")
        return redirect("claim_detail", claim_id=claim.id)
    if request.method == "POST":
        _audit(claim, request.user, "CLAIM_DELETED", "Draft deleted")
        claim.deleted_by = request.user
        claim.delete()
        messages.success(request, "Brouillon supprime.")
        return redirect("claim_list")
    return redirect("claim_detail", claim_id=claim.id)


@login_required
def claim_detail(request, claim_id):
    claim = get_object_or_404(
        Claim.objects.select_related(
            "patient", "category", "provider",
            "patient__ipm", "patient__coverage_plan",
            "provider__staff_profile__hospital",
        ),
        id=claim_id,
    )
    if not _can_access_claim(request.user, claim):
        return HttpResponseForbidden("Access denied.")

    upload_form = ClaimDocumentUploadForm()

    if request.method == "POST":
        action = request.POST.get("action", "").strip()

        if action == "submit":
            if not _can_edit_claim(request.user, claim):
                return HttpResponseForbidden("Seul le prestataire peut soumettre le dossier.")
            try:
                ClaimStateMachine.submit(claim, request.user)
                send_claim_notifications(claim, request)
                messages.success(request, "Claim soumise.")
            except ClaimTransitionError as exc:
                messages.warning(request, str(exc))
            return redirect("claim_detail", claim_id=claim.id)

        if action == "lock":
            if not request.user.is_superuser:
                return HttpResponseForbidden("Only superadmin can lock claims.")
            try:
                ClaimStateMachine.lock(claim, request.user)
                send_claim_notifications(claim, request)
                messages.success(request, "Claim verrouillee et lien patient genere.")
            except ClaimTransitionError as exc:
                messages.warning(request, str(exc))
            return redirect("claim_detail", claim_id=claim.id)

        if action == "resend_notification":
            channel = (request.POST.get("channel") or "").strip()
            if channel and channel in [c.value for c in NotificationChannel]:
                send_claim_notifications(claim, request, channels=[channel])
                messages.success(request, f"Renvoyé par {channel}.")
            else:
                send_claim_notifications(claim, request)
                messages.success(request, "Notifications renvoyées pour tous les canaux actifs.")
            return redirect("claim_detail", claim_id=claim.id)

        if action == "upload_document":
            if not _can_edit_claim(request.user, claim):
                return HttpResponseForbidden("Seul le prestataire peut ajouter des documents.")
            if claim.status != ClaimStatus.DRAFT:
                messages.warning(request, "Upload autorise uniquement en DRAFT.")
                return redirect("claim_detail", claim_id=claim.id)
            upload_form = ClaimDocumentUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                files = request.FILES.getlist("documents")
                doc_type = upload_form.cleaned_data.get("document_type", "AUTRE")
                for f in files:
                    ClaimDocument.objects.create(
                        claim=claim, file=f, original_name=f.name, document_type=doc_type
                    )
                _audit(claim, request.user, "DOCUMENTS_UPLOADED", f"{len(files)} file(s) uploaded")
                messages.success(request, f"{len(files)} document(s) ajoute(s).")
            else:
                messages.warning(request, "Impossible d'uploader le document.")
            return redirect("claim_detail", claim_id=claim.id)

    verify_url = None
    if claim.patient_token:
        verify_url = request.build_absolute_uri(reverse("patient_verify_public", args=[claim.patient_token]))

    documents = claim.documents.order_by("-uploaded_at")
    audit_logs = claim.audit_logs.select_related("actor").order_by("-created_at")[:30]
    notification_logs = claim.notification_logs.order_by("-sent_at")[:20]
    snapshot = claim.snapshot_json or {}
    try:
        provider_hospital = claim.provider.staff_profile.hospital
    except ObjectDoesNotExist:
        provider_hospital = None
    provider_payment_options = (
        list(provider_hospital.payment_options.select_related("payment_method"))
        if provider_hospital else []
    )
    return render(
        request,
        "claims/detail.html",
        {
            "claim": claim,
            "verify_url": verify_url,
            "documents": documents,
            "audit_logs": audit_logs,
            "notification_logs": notification_logs,
            "upload_form": upload_form,
            "provider_hospital": provider_hospital,
            "provider_payment_options": provider_payment_options,
            "user_role": get_user_role(request.user),
            "can_edit_claim": _can_edit_claim(request.user, claim),
            "ipm_share": snapshot.get("ipm_share"),
            "patient_share": snapshot.get("patient_share"),
            "coverage_percent": snapshot.get("coverage_percent"),
        },
    )


# ──────────────────────────────────────────────
# API Coverage (JSON)
# ──────────────────────────────────────────────

@login_required
def api_coverage(request):
    """Return coverage % for patient + category via CoveragePlan lookup."""
    patient_id = request.GET.get("patient_id", "").strip()
    category_id = request.GET.get("category_id", "").strip()
    if not patient_id or not category_id:
        return JsonResponse({"coverage_percent": None, "error": "patient_id et category_id requis"})
    try:
        patient = Patient.objects.select_related("ipm", "coverage_plan").get(id=int(patient_id))
        rule = None
        if patient.coverage_plan:
            rule = CoverageRule.objects.filter(
                coverage_plan=patient.coverage_plan, category_id=int(category_id), is_active=True
            ).first()
        coverage = float(rule.coverage_percent) if rule else 0.0
        return JsonResponse({
            "coverage_percent": coverage,
            "ipm_name": patient.ipm.name,
            "formule": patient.coverage_plan.name if patient.coverage_plan else "",
        })
    except (Patient.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"coverage_percent": None, "error": "Données invalides"})


# ──────────────────────────────────────────────
# IPM CRUD
# ──────────────────────────────────────────────

@login_required
def ipm_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superadmin can access IPM management.")
    ipms = IPM.objects.order_by("name")
    return render(request, "ipm/list.html", {"ipms": ipms})


@login_required
def ipm_delete(request, ipm_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superadmin can delete IPM.")
    ipm = get_object_or_404(IPM, id=ipm_id)
    if request.method != "POST":
        return redirect("ipm_list")
    ipm.deleted_by = request.user
    ipm.delete()  # soft delete
    messages.success(request, "IPM supprimée (suppression logique).")
    return redirect("ipm_list")


@login_required
def ipm_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superadmin can create IPM.")
    form = IPMForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "IPM créée avec succès.")
        return redirect("ipm_list")
    return render(request, "ipm/form.html", {"form": form, "title": "Nouvelle IPM"})


@login_required
def ipm_create_ajax(request):
    """Création rapide d'une IPM (AJAX). Retourne JSON {id, name}. Réservé superadmin. Compléter la fiche depuis la liste IPM."""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Accès refusé."}, status=403)
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)
    name = (request.POST.get("name") or "").strip()
    if not name:
        return JsonResponse({"error": "Le nom est requis."}, status=400)
    if IPM.objects.filter(name__iexact=name).exists():
        return JsonResponse({"error": "Une IPM avec ce nom existe déjà."}, status=400)
    code = (request.POST.get("code") or "").strip() or None
    if code and IPM.objects.filter(code__iexact=code).exists():
        return JsonResponse({"error": "Une IPM avec ce code existe déjà."}, status=400)
    ipm = IPM.objects.create(name=name, code=code, is_active=True)
    return JsonResponse({"id": ipm.id, "name": ipm.name})


def _hospital_edit_payment_options(hospital, request_post, request=None):
    """Sauvegarde des moyens de paiement de l'établissement (hôpital/pharmacie). Soft delete si décoché."""
    active_pm_ids = set()
    for key, value in request_post.items():
        if key.startswith("payment_") and key.endswith("_used") and value:
            try:
                pm_id = int(key.replace("payment_", "").replace("_used", ""))
                active_pm_ids.add(pm_id)
            except ValueError:
                pass
    existing = {o.payment_method_id: o for o in hospital.payment_options.select_related("payment_method")}
    deleted_by = request.user if request and request.user.is_authenticated else None

    for pm in PaymentMethod.objects.filter(is_active=True).order_by("name"):
        used = pm.id in active_pm_ids
        prefix = f"payment_{pm.id}"
        if used:
            opt = existing.get(pm.id)
            if opt is None:
                opt = EstablishmentPaymentOption.all_objects.filter(hospital=hospital, payment_method=pm).first()
                if opt:
                    opt.is_deleted = False
                    opt.deleted_at = None
                    opt.deleted_by = None
                else:
                    opt = EstablishmentPaymentOption(hospital=hospital, payment_method=pm)
            opt.phone = (request_post.get(f"{prefix}_phone") or "").strip()[:30]
            opt.iban = (request_post.get(f"{prefix}_iban") or "").strip()[:40]
            opt.bank_name = (request_post.get(f"{prefix}_bank_name") or "").strip()[:120]
            opt.payee_name = (request_post.get(f"{prefix}_payee_name") or "").strip()[:120]
            opt.reference_notes = (request_post.get(f"{prefix}_reference_notes") or "").strip()[:255]
            opt.is_active = True
            opt.save()
        else:
            EstablishmentPaymentOption.objects.filter(hospital=hospital, payment_method=pm).update(
                is_deleted=True, deleted_at=timezone.now(), deleted_by=deleted_by
            )


def _ipm_edit_payment_options(ipm, request_post, request=None):
    """Sauvegarde des moyens de paiement acceptés par l'IPM (champs selon type). Soft delete si décoché."""
    active_pm_ids = set()
    for key, value in request_post.items():
        if key.startswith("payment_") and key.endswith("_used") and value:
            try:
                pm_id = int(key.replace("payment_", "").replace("_used", ""))
                active_pm_ids.add(pm_id)
            except ValueError:
                pass
    existing = {o.payment_method_id: o for o in ipm.payment_options.select_related("payment_method")}
    deleted_by = request.user if request and request.user.is_authenticated else None

    for pm in PaymentMethod.objects.filter(is_active=True).order_by("name"):
        used = pm.id in active_pm_ids
        prefix = f"payment_{pm.id}"
        if used:
            opt = existing.get(pm.id)
            if opt is None:
                opt = IPMPaymentOption.all_objects.filter(ipm=ipm, payment_method=pm).first()
                if opt:
                    opt.is_deleted = False
                    opt.deleted_at = None
                    opt.deleted_by = None
                else:
                    opt = IPMPaymentOption(ipm=ipm, payment_method=pm)
            opt.phone = (request_post.get(f"{prefix}_phone") or "").strip()[:30]
            opt.iban = (request_post.get(f"{prefix}_iban") or "").strip()[:40]
            opt.bank_name = (request_post.get(f"{prefix}_bank_name") or "").strip()[:120]
            opt.payee_name = (request_post.get(f"{prefix}_payee_name") or "").strip()[:120]
            opt.reference_notes = (request_post.get(f"{prefix}_reference_notes") or "").strip()[:255]
            opt.is_active = True
            opt.save()
        else:
            IPMPaymentOption.objects.filter(ipm=ipm, payment_method=pm).update(
                is_deleted=True, deleted_at=timezone.now(), deleted_by=deleted_by
            )


@login_required
def ipm_edit(request, ipm_id):
    ipm = get_object_or_404(IPM, id=ipm_id)
    scope = _ipm_scope_queryset(request.user)
    if not request.user.is_superuser and not scope.filter(pk=ipm.pk).exists():
        return HttpResponseForbidden("Vous ne pouvez modifier que votre propre IPM.")
    form = IPMForm(request.POST or None, instance=ipm)
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by("name")
    option_by_pm_id = {o.payment_method_id: o for o in ipm.payment_options.select_related("payment_method")}
    payment_method_options = [(pm, option_by_pm_id.get(pm.id)) for pm in payment_methods]

    is_own_ipm = not request.user.is_superuser
    if request.method == "POST":
        if is_own_ipm:
            # IPM Admin : on ne met à jour que les moyens de paiement, pas l'identité de l'IPM.
            _ipm_edit_payment_options(ipm, request.POST, request)
            messages.success(request, "Moyens de paiement mis à jour.")
            return redirect("claim_list")
        if form.is_valid():
            form.save()
            _ipm_edit_payment_options(ipm, request.POST, request)
            messages.success(request, "IPM et moyens de paiement mis à jour.")
            return redirect("ipm_list")
    return render(
        request,
        "ipm/form.html",
        {
            "form": form,
            "title": f"Modifier IPM: {ipm.name}" if not is_own_ipm else "Mon IPM",
            "ipm": ipm,
            "payment_method_options": payment_method_options,
            "is_own_ipm": is_own_ipm,
        },
    )


# ──────────────────────────────────────────────
# Hospital (Hôpitaux / Pharmacies) CRUD
# ──────────────────────────────────────────────

@login_required
def hospital_list(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Accès réservé au superadmin.")
    hospitals = Hospital.objects.order_by("name")
    return render(request, "hospital/list.html", {"hospitals": hospitals})


@login_required
def hospital_delete(request, hospital_id):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Accès refusé.")
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method != "POST":
        return redirect("hospital_list")
    hospital.deleted_by = request.user
    hospital.delete()
    messages.success(request, "Établissement supprimé (suppression logique).")
    return redirect("hospital_list")


@login_required
def hospital_create(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Accès réservé au superadmin.")
    form = HospitalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hôpital / Pharmacie créé avec succès.")
        return redirect("hospital_list")
    return render(request, "hospital/form.html", {"form": form, "title": "Nouvel hôpital / pharmacie"})


@login_required
def hospital_create_ajax(request):
    """Création rapide d'un établissement (AJAX). Retourne JSON {id, name}. Réservé superadmin."""
    if not _superadmin_only(request.user):
        return JsonResponse({"error": "Accès refusé."}, status=403)
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)
    name = (request.POST.get("name") or "").strip()
    if not name:
        return JsonResponse({"error": "Le nom est requis."}, status=400)
    establishment_type = (request.POST.get("establishment_type") or "").strip() or EstablishmentType.HOSPITAL
    if establishment_type not in (EstablishmentType.HOSPITAL, EstablishmentType.PHARMACY):
        establishment_type = EstablishmentType.HOSPITAL
    if Hospital.objects.filter(name__iexact=name).filter(is_deleted=False).exists():
        return JsonResponse({"error": "Un établissement avec ce nom existe déjà."}, status=400)
    code = (request.POST.get("code") or "").strip() or None
    if code and Hospital.objects.filter(code__iexact=code).filter(is_deleted=False).exists():
        return JsonResponse({"error": "Un établissement avec ce code existe déjà."}, status=400)
    hospital = Hospital.objects.create(
        name=name,
        code=code,
        establishment_type=establishment_type,
        is_active=True,
    )
    return JsonResponse({"id": hospital.id, "name": hospital.name})


@login_required
def hospital_edit(request, hospital_id):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Accès refusé.")
    hospital = get_object_or_404(Hospital, id=hospital_id)
    form = HospitalForm(request.POST or None, instance=hospital)
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by("name")
    option_by_pm_id = {o.payment_method_id: o for o in hospital.payment_options.select_related("payment_method")}
    payment_method_options = [(pm, option_by_pm_id.get(pm.id)) for pm in payment_methods]

    if request.method == "POST":
        if form.is_valid():
            form.save()
            _hospital_edit_payment_options(hospital, request.POST, request)
            messages.success(request, "Établissement et moyens de paiement mis à jour.")
            return redirect("hospital_list")
    return render(
        request,
        "hospital/form.html",
        {
            "form": form,
            "title": f"Modifier : {hospital.name}",
            "hospital": hospital,
            "payment_method_options": payment_method_options,
        },
    )


@login_required
def my_establishment_payment_options(request):
    """Permet aux cliniques/hôpitaux/pharmacies de configurer les moyens de paiement de leur établissement (sans modifier l'identité de l'établissement)."""
    try:
        profile = request.user.staff_profile
    except ObjectDoesNotExist:
        profile = None
    if not profile or profile.role not in (UserRole.DOCTOR, UserRole.PHARMACY):
        return HttpResponseForbidden("Accès réservé aux prestataires (médecin, clinique, pharmacie).")
    hospital = getattr(profile, "hospital", None)
    if not hospital:
        messages.warning(
            request,
            "Aucun établissement n'est associé à votre compte. Contactez l'administrateur pour configurer votre profil.",
        )
        return redirect("provider_dashboard")
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by("name")
    option_by_pm_id = {o.payment_method_id: o for o in hospital.payment_options.select_related("payment_method")}
    payment_method_options = [(pm, option_by_pm_id.get(pm.id)) for pm in payment_methods]

    if request.method == "POST":
        _hospital_edit_payment_options(hospital, request.POST, request)
        messages.success(request, "Moyens de paiement enregistrés.")
        return redirect("my_establishment_payment_options")
    return render(
        request,
        "hospital/my_payment_options.html",
        {
            "hospital": hospital,
            "payment_method_options": payment_method_options,
        },
    )


# ──────────────────────────────────────────────
# CoveragePlan (Formule) CRUD
# ──────────────────────────────────────────────

@login_required
def plan_list(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    plans = CoveragePlan.objects.select_related("ipm").order_by("ipm__name", "name")
    scope = _ipm_scope_queryset(request.user)
    if not request.user.is_superuser:
        plans = plans.filter(ipm__in=scope)
    q = request.GET.get("q", "").strip()
    if q:
        plans = plans.filter(Q(name__icontains=q) | Q(ipm__name__icontains=q))
    return render(request, "formule/list.html", {"plans": plans[:500], "query": q})


@login_required
def plan_create(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    scope = _ipm_scope_queryset(request.user)
    forced_ipm = None
    if not request.user.is_superuser:
        forced_ipm = scope.first()
        if forced_ipm is None:
            return HttpResponseForbidden("Aucune IPM liée à votre profil.")
    form = CoveragePlanForm(
        request.POST or None,
        ipm_queryset=scope.filter(is_active=True).order_by("name"),
        forced_ipm=forced_ipm,
    )
    categories = list(Category.objects.filter(is_active=True).order_by("name"))
    category_rows = _build_category_rule_state(
        categories,
        request_post=request.POST if request.method == "POST" else None,
    )
    if request.method == "POST" and form.is_valid():
        payload, errors = _extract_plan_rule_payload(request, categories)
        if errors:
            for msg in errors[:5]:
                messages.error(request, msg)
        else:
            plan = form.save()
            created_count = 0
            for category_id, percent in payload.items():
                CoverageRule.objects.create(
                    coverage_plan=plan,
                    category_id=category_id,
                    coverage_percent=percent,
                    is_active=True,
                )
                created_count += 1
            if created_count:
                messages.success(request, f"Formule créée avec {created_count} règle(s) de couverture.")
            else:
                messages.success(request, "Formule créée. Vous pouvez ajouter les règles ensuite.")
            return redirect("plan_list")
    return render(
        request,
        "formule/form.html",
        {
            "form": form,
            "title": "Nouvelle formule",
            "forced_ipm": forced_ipm,
            "category_rows": category_rows,
        },
    )


@login_required
def plan_edit(request, plan_id):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    scope = _ipm_scope_queryset(request.user)
    plan = get_object_or_404(CoveragePlan.objects.select_related("ipm"), id=plan_id)
    if not request.user.is_superuser and not scope.filter(id=plan.ipm_id).exists():
        return HttpResponseForbidden("Access denied.")
    forced_ipm = None if request.user.is_superuser else plan.ipm
    form = CoveragePlanForm(
        request.POST or None,
        instance=plan,
        ipm_queryset=scope.filter(is_active=True).order_by("name"),
        forced_ipm=forced_ipm,
    )
    categories = list(Category.objects.filter(is_active=True).order_by("name"))
    existing_rules = {
        r.category_id: r
        for r in CoverageRule.objects.filter(coverage_plan=plan).select_related("category")
    }
    category_rows = _build_category_rule_state(
        categories,
        request_post=request.POST if request.method == "POST" else None,
        existing_rules=existing_rules,
    )
    if request.method == "POST" and form.is_valid():
        payload, errors = _extract_plan_rule_payload(request, categories)
        if errors:
            for msg in errors[:5]:
                messages.error(request, msg)
        else:
            plan = form.save()
            touched = 0
            deactivated = 0
            selected_ids = set(payload.keys())
            existing = {
                r.category_id: r
                for r in CoverageRule.objects.filter(coverage_plan=plan)
            }
            for category_id, percent in payload.items():
                rule = existing.get(category_id)
                if rule:
                    changed = False
                    if rule.coverage_percent != percent:
                        rule.coverage_percent = percent
                        changed = True
                    if not rule.is_active:
                        rule.is_active = True
                        changed = True
                    if changed:
                        rule.save(update_fields=["coverage_percent", "is_active"])
                    touched += 1
                else:
                    CoverageRule.objects.create(
                        coverage_plan=plan,
                        category_id=category_id,
                        coverage_percent=percent,
                        is_active=True,
                    )
                    touched += 1
            for category_id, rule in existing.items():
                if category_id not in selected_ids and rule.is_active:
                    rule.is_active = False
                    rule.save(update_fields=["is_active"])
                    deactivated += 1
            messages.success(
                request,
                f"Formule mise à jour. {touched} règle(s) active(s), {deactivated} désactivée(s).",
            )
            return redirect("plan_list")
    return render(
        request,
        "formule/form.html",
        {
            "form": form,
            "title": f"Modifier formule: {plan.name}",
            "plan": plan,
            "forced_ipm": forced_ipm,
            "category_rows": category_rows,
        },
    )


# ──────────────────────────────────────────────
# Patient CRUD
# ──────────────────────────────────────────────

@login_required
def patient_list(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    patients = Patient.objects.select_related("ipm", "coverage_plan").order_by("-created_at")
    scope = _ipm_scope_queryset(request.user)
    if not request.user.is_superuser:
        patients = patients.filter(ipm__in=scope)
    q = request.GET.get("q", "").strip()
    if q:
        patients = patients.filter(
            Q(full_name__icontains=q)
            | Q(member_number__icontains=q)
            | Q(phone__icontains=q)
            | Q(id_number__icontains=q)
        )
    return render(request, "patient/list.html", {"patients": patients[:500], "query": q})


@login_required
def patient_create(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    scope = _ipm_scope_queryset(request.user)
    # IPM Admin : une seule IPM, on la force et on masque le champ ; formules = uniquement les siennes
    forced_ipm = None
    show_ipm_field = request.user.is_superuser
    if not request.user.is_superuser:
        forced_ipm = scope.first()
        if is_ipm_admin(request.user) and not scope.exists():
            try:
                profile = request.user.staff_profile
                ipm_name = (getattr(profile, "ipm_name", None) or "").strip()
            except ObjectDoesNotExist:
                ipm_name = ""
            if ipm_name:
                messages.error(
                    request,
                    "Le nom d'IPM configuré dans votre profil (« %s ») ne correspond à aucune IPM en base. "
                    "Contactez l'administrateur pour corriger votre profil ou créer cette IPM." % ipm_name,
                )
            else:
                messages.error(
                    request,
                    "Votre compte n'est pas associé à une IPM. Contactez l'administrateur pour configurer votre profil.",
                )
            return redirect("patient_list")
    plan_scope = _plan_scope_queryset(request.user).filter(is_active=True).order_by("ipm__name", "name")
    form = PatientForm(
        request.POST or None,
        ipm_queryset=scope.filter(is_active=True).order_by("name"),
        plan_queryset=plan_scope,
        forced_ipm=forced_ipm,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Patient créé avec succès.")
        return redirect("patient_list")
    return render(
        request,
        "patient/form.html",
        {
            "form": form,
            "title": "Nouveau patient",
            "forced_ipm": forced_ipm,
            "show_ipm_field": show_ipm_field,
        },
    )


@login_required
def patient_edit(request, patient_id):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    scope = _ipm_scope_queryset(request.user)
    patient = get_object_or_404(Patient.objects.select_related("ipm", "coverage_plan"), id=patient_id)
    if not request.user.is_superuser and not scope.filter(id=patient.ipm_id).exists():
        return HttpResponseForbidden("Access denied.")
    forced_ipm = None
    show_ipm_field = request.user.is_superuser
    if not request.user.is_superuser:
        forced_ipm = scope.first()
        if is_ipm_admin(request.user) and not scope.exists():
            try:
                profile = request.user.staff_profile
                ipm_name = (getattr(profile, "ipm_name", None) or "").strip()
            except ObjectDoesNotExist:
                ipm_name = ""
            if ipm_name:
                messages.error(
                    request,
                    "Le nom d'IPM configuré dans votre profil (« %s ») ne correspond à aucune IPM en base. "
                    "Contactez l'administrateur pour corriger votre profil ou créer cette IPM." % ipm_name,
                )
            else:
                messages.error(
                    request,
                    "Votre compte n'est pas associé à une IPM. Contactez l'administrateur pour configurer votre profil.",
                )
            return redirect("patient_list")
    plan_scope = _plan_scope_queryset(request.user).filter(is_active=True).order_by("ipm__name", "name")
    form = PatientForm(
        request.POST or None,
        request.FILES or None,
        instance=patient,
        ipm_queryset=scope.filter(is_active=True).order_by("name"),
        plan_queryset=plan_scope,
        forced_ipm=forced_ipm,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Patient mis à jour.")
        return redirect("patient_list")
    return render(
        request,
        "patient/form.html",
        {
            "form": form,
            "title": f"Modifier patient: {patient.full_name}",
            "patient": patient,
            "forced_ipm": forced_ipm,
            "show_ipm_field": show_ipm_field,
        },
    )


# ──────────────────────────────────────────────
# Coverage Rule CRUD
# ──────────────────────────────────────────────

@login_required
def coverage_rule_list(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    rules = CoverageRule.objects.select_related("coverage_plan", "coverage_plan__ipm", "category").order_by(
        "coverage_plan__ipm__name", "coverage_plan__name", "category__name"
    )
    scope = _ipm_scope_queryset(request.user)
    if not request.user.is_superuser:
        rules = rules.filter(coverage_plan__ipm__in=scope)

    plan_filter = request.GET.get("plan", "").strip()
    type_filter = request.GET.get("type", "").strip()
    q = request.GET.get("q", "").strip()

    if plan_filter:
        rules = rules.filter(coverage_plan_id=plan_filter)
    if type_filter == "PHARMACY":
        rules = rules.filter(category__is_pharmacy=True)
    elif type_filter == "SERVICE":
        rules = rules.filter(category__is_pharmacy=False)
    if q:
        rules = rules.filter(
            Q(coverage_plan__ipm__name__icontains=q) | Q(coverage_plan__name__icontains=q) | Q(category__name__icontains=q)
        )

    rules = rules[:500]
    plan_choices = _plan_scope_queryset(request.user).filter(is_active=True).order_by("ipm__name", "name")
    context = {
        "rules": rules,
        "query": q,
        "type_filter": type_filter,
        "plan_filter": plan_filter,
        "plan_choices": plan_choices,
        "total_rules": len(rules),
        "active_rules": sum(1 for r in rules if r.is_active),
    }
    return render(request, "coverage/list.html", context)


@login_required
def coverage_rule_create(request):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    plans = _plan_scope_queryset(request.user).filter(is_active=True).order_by("ipm__name", "name")
    forced_plan = None
    if not request.user.is_superuser:
        forced_plan = plans.first()
        if forced_plan is None:
            messages.warning(
                request,
                "Créez d'abord au moins une formule pour votre IPM afin de pouvoir ajouter des règles de couverture.",
            )
            return redirect("plan_create")
    form = CoverageRuleForm(
        request.POST or None,
        plan_queryset=plans,
        forced_plan=forced_plan,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Règle de couverture créée.")
        return redirect("coverage_rule_list")
    return render(
        request,
        "coverage/form.html",
        {"form": form, "title": "Nouvelle règle de couverture", "forced_plan": forced_plan},
    )


@login_required
def coverage_rule_edit(request, rule_id):
    if not _can_manage_master_data(request.user):
        return HttpResponseForbidden("Access denied.")
    rule = get_object_or_404(CoverageRule.objects.select_related("coverage_plan", "coverage_plan__ipm", "category"), id=rule_id)
    scope = _ipm_scope_queryset(request.user)
    if not request.user.is_superuser and not scope.filter(id=rule.coverage_plan.ipm_id).exists():
        return HttpResponseForbidden("Access denied.")
    plans = _plan_scope_queryset(request.user).filter(is_active=True).order_by("ipm__name", "name")
    forced_plan = None if request.user.is_superuser else rule.coverage_plan
    form = CoverageRuleForm(
        request.POST or None,
        instance=rule,
        plan_queryset=plans,
        forced_plan=forced_plan,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Règle de couverture mise à jour.")
        return redirect("coverage_rule_list")
    plan_label = f"{rule.coverage_plan.ipm.name} / {rule.coverage_plan.name}"
    return render(
        request,
        "coverage/form.html",
        {"form": form, "title": f"Modifier couverture: {plan_label} / {rule.category.name}", "rule": rule, "forced_plan": forced_plan},
    )


# ──────────────────────────────────────────────
# Category CRUD
# ──────────────────────────────────────────────

DEFAULT_CATEGORIES = [
    ("Consultation generale", False),
    ("Consultation specialisee", False),
    ("Hospitalisation", False),
    ("Urgences", False),
    ("Chirurgie", False),
    ("Anesthesie", False),
    ("Imagerie", False),
    ("Radiologie", False),
    ("Echographie", False),
    ("Scanner", False),
    ("IRM", False),
    ("Laboratoire", False),
    ("Biologie", False),
    ("Analyse sanguine", False),
    ("Soins dentaires", False),
    ("Ophtalmologie", False),
    ("Maternite", False),
    ("Pediatrie", False),
    ("Kinesitherapie", False),
    ("Vaccination", False),
    ("Medicaments generiques", True),
    ("Medicaments de marque", True),
    ("Dispositifs medicaux", True),
    ("Consommables medicaux", True),
]


@login_required
def category_list(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can access categories.")
    categories = Category.objects.order_by("name")
    return render(request, "category/list.html", {"categories": categories})


@login_required
def category_seed_defaults(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can seed categories.")

    if request.method == "GET":
        existing_names = set(Category.objects.values_list("name", flat=True))
        items = [
            {"name": name, "is_pharmacy": is_pharmacy, "exists": name in existing_names}
            for name, is_pharmacy in DEFAULT_CATEGORIES
        ]
        return render(request, "category/seed.html", {"items": items})

    # POST — import selected
    selected = request.POST.getlist("categories")
    if not selected:
        messages.warning(request, "Aucune catégorie sélectionnée.")
        return redirect("category_seed_defaults")

    lookup = {name: is_pharmacy for name, is_pharmacy in DEFAULT_CATEGORIES}
    created_count = 0
    for name in selected:
        is_pharmacy = lookup.get(name, False)
        _, created = Category.objects.get_or_create(
            name=name,
            defaults={"is_pharmacy": is_pharmacy, "is_active": True},
        )
        if created:
            created_count += 1

    messages.success(request, f"{created_count} catégorie(s) ajoutée(s).")
    return redirect("category_list")


@login_required
def category_create(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can create categories.")
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Catégorie créée avec succès.")
        return redirect("category_list")
    return render(request, "category/form.html", {"form": form, "title": "Nouvelle catégorie"})


@login_required
def category_edit(request, category_id):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can edit categories.")
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Catégorie mise à jour.")
        return redirect("category_list")
    return render(request, "category/form.html", {"form": form, "title": f"Modifier catégorie: {category.name}"})


# ──────────────────────────────────────────────
# PaymentMethod CRUD
# ──────────────────────────────────────────────

@login_required
def payment_method_list(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Réservé au superadmin.")
    methods = PaymentMethod.objects.order_by("name")
    return render(request, "payment_method/list.html", {"payment_methods": methods})


@login_required
def payment_method_create(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Réservé au superadmin.")
    form = PaymentMethodForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Moyen de paiement ajouté.")
        return redirect("payment_method_list")
    return render(request, "payment_method/form.html", {"form": form, "title": "Nouveau moyen de paiement"})


@login_required
def payment_method_edit(request, payment_method_id):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Réservé au superadmin.")
    pm = get_object_or_404(PaymentMethod, id=payment_method_id)
    form = PaymentMethodForm(request.POST or None, instance=pm)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Moyen de paiement mis à jour.")
        return redirect("payment_method_list")
    return render(request, "payment_method/form.html", {"form": form, "title": f"Modifier: {pm.name}", "payment_method": pm})


# ──────────────────────────────────────────────
# User CRUD
# ──────────────────────────────────────────────

@login_required
def user_list(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can manage users.")
    # Exclure les utilisateurs dont le profil a été soft-deleted
    users = (
        User.objects.select_related("staff_profile", "staff_profile__hospital")
        .filter(Q(staff_profile__isnull=True) | Q(staff_profile__is_deleted=False))
        .order_by("username")
    )
    q = request.GET.get("q", "").strip()
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    return render(request, "users/list.html", {"users": users[:500], "query": q})


@login_required
def user_create(request):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can create users.")
    form = UserManagementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Utilisateur créé avec succès.")
        return redirect("user_list")
    return render(request, "users/form.html", {"form": form, "title": "Nouvel utilisateur"})


@login_required
def user_edit(request, user_id):
    # Précharger staff_profile uniquement (éviter staff_profile__ipm : selon l'ordre de chargement des apps,
    # la FK ipm peut ne pas être visible pour select_related ; profile.ipm sera chargé à l'accès dans le formulaire)
    target = get_object_or_404(
        User.objects.select_related("staff_profile"),
        id=user_id,
    )
    # Superadmin peut modifier n'importe qui ; tout le monde peut modifier son propre profil (nom, email, MDP).
    can_edit = request.user.is_superuser or (target.id == request.user.id)
    if not can_edit:
        return HttpResponseForbidden("Vous ne pouvez pas modifier cet utilisateur.")
    if getattr(target, "staff_profile", None) and getattr(target.staff_profile, "is_deleted", False):
        raise Http404("Cet utilisateur a été supprimé.")
    is_self = target.id == request.user.id
    if is_self:
        form = ProfileSelfEditForm(request.POST or None, user=target)
    else:
        form = UserManagementForm(request.POST or None, instance=target)
    if request.method == "POST" and form.is_valid():
        if is_self:
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("claim_list")
        form.save()
        messages.success(request, "Utilisateur mis à jour.")
        return redirect("user_list")
    return render(
        request,
        "users/form.html",
        {"form": form, "title": "Mon profil" if is_self else f"Modifier utilisateur: {target.username}", "target_user": target, "is_self_edit": is_self},
    )


@login_required
def user_delete(request, user_id):
    if not _superadmin_only(request.user):
        return HttpResponseForbidden("Only superadmin can delete users.")
    target = get_object_or_404(User, id=user_id)
    if request.user.id == target.id:
        messages.warning(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect("user_list")
    if request.method != "POST":
        return redirect("user_list")
    if getattr(target, "staff_profile", None):
        target.staff_profile.deleted_by = request.user
        target.staff_profile.delete()  # soft delete + user.is_active = False
    else:
        target.is_active = False
        target.save(update_fields=["is_active"])
    messages.success(request, "Utilisateur supprimé (suppression logique).")
    return redirect("user_list")


# ──────────────────────────────────────────────
# Notifications (config canaux : Email, SMS, WhatsApp)
# ──────────────────────────────────────────────

@login_required
def notification_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Réservé au superadmin.")
    channels = []
    for ch in NotificationChannel:
        cfg, _ = NotificationChannelConfig.objects.get_or_create(channel=ch.value, defaults={"is_active": False})
        channels.append(cfg)
    return render(request, "notifications/list.html", {"channels": channels})


@login_required
def notification_edit(request, channel_code):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Réservé au superadmin.")
    if channel_code not in [c.value for c in NotificationChannel]:
        raise Http404("Canal inconnu.")
    config, _ = NotificationChannelConfig.objects.get_or_create(channel=channel_code, defaults={"is_active": False})
    form = NotificationChannelConfigForm(channel=channel_code, config_instance=config, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Configuration {config.get_channel_display()} enregistrée.")
        return redirect("notification_list")
    return render(
        request,
        "notifications/edit.html",
        {"form": form, "config": config, "channel_code": channel_code},
    )


@login_required
def notification_test(request, channel_code):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Réservé au superadmin.")
    if channel_code not in [c.value for c in NotificationChannel]:
        raise Http404("Canal inconnu.")
    config = get_object_or_404(NotificationChannelConfig, channel=channel_code)
    destination = (request.POST.get("test_destination") or request.GET.get("destination") or "").strip()
    if request.method != "POST" and not destination:
        return redirect("notification_edit", channel_code=channel_code)
    now = timezone.now()
    config.last_tested_at = now
    error_msg = ""
    if channel_code == NotificationChannel.EMAIL.value:
        if not destination or "@" not in destination:
            error_msg = "Indiquez une adresse email valide."
        else:
            cfg = config.config or {}
            try:
                port = int(cfg.get("port") or 587)
                use_ssl = port == 465
                backend = EmailBackend(
                    host=cfg.get("host") or "localhost",
                    port=port,
                    username=cfg.get("user") or None,
                    password=cfg.get("password") or None,
                    use_tls=False if use_ssl else bool(cfg.get("use_tls", True)),
                    use_ssl=use_ssl,
                    fail_silently=False,
                    timeout=20,
                )
                # Utiliser le modèle de message configuré si présent
                test_ctx = {"patient_name": "Test Utilisateur", "verify_link": "https://exemple.com/verify/xxx", "claim_id": "123"}
                def replace_placeholders(text):
                    if not text:
                        return text
                    for k, v in test_ctx.items():
                        text = text.replace("{{ " + k + " }}", str(v)).replace("{{" + k + "}}", str(v))
                    return text
                subject = replace_placeholders(cfg.get("subject_template") or "[REMEDY] Test de notification")
                body = replace_placeholders(cfg.get("body_template") or "Ceci est un email de test envoyé depuis la plateforme REMEDY.")
                msg = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=cfg.get("from_email") or "noreply@remedy.local",
                    to=[destination],
                    connection=backend,
                )
                msg.send()
            except Exception as e:
                error_msg = str(e)
    elif channel_code == NotificationChannel.SMS.value:
        error_msg = "Test SMS non implémenté : configurez une API SMS et appelez-la ici."
    elif channel_code == NotificationChannel.WHATSAPP.value:
        error_msg = "Test WhatsApp non implémenté."
    config.last_test_error = error_msg
    config.save(update_fields=["last_tested_at", "last_test_error"])
    if error_msg:
        messages.error(request, f"Échec du test : {error_msg}")
    else:
        messages.success(request, f"Test envoyé vers {destination}.")
    return redirect("notification_edit", channel_code=channel_code)


# ──────────────────────────────────────────────
# Patient Verify (public)
# ──────────────────────────────────────────────

@login_not_required
def patient_verify(request, token):
    claim = get_object_or_404(Claim, patient_token=token)
    now = timezone.now()
    is_expired = bool(claim.token_expires_at and claim.token_expires_at < now)
    is_used = bool(claim.token_used_at)

    def _link_used_outcome():
        if is_expired:
            return "expired"
        if is_used and claim.status == ClaimStatus.READY_FOR_PAYMENT:
            return "already_confirmed"
        if is_used and claim.status in (ClaimStatus.BLOCKED, ClaimStatus.DISPUTED):
            return "already_disputed"
        if is_used:
            return "already_used"
        return "invalid"

    if request.method == "POST":
        action = request.POST.get("action", "").strip()
        if claim.status != ClaimStatus.LOCKED or is_expired or is_used:
            return render(
                request,
                "patient/verify.html",
                {"claim": claim, "invalid": True, "link_used_outcome": _link_used_outcome()},
            )

        if action == "confirm":
            try:
                ClaimStateMachine.patient_confirm(claim)
            except ClaimTransitionError:
                return render(request, "patient/verify.html", {"claim": claim, "invalid": True})
            return render(request, "patient/verify.html", {"claim": claim, "done": "confirmed"})

        if action == "dispute":
            dispute_reason = (request.POST.get("dispute_reason") or "").strip()
            if not dispute_reason:
                snapshot = claim.snapshot_json or {}
                profile = getattr(claim.provider, "staff_profile", None)
                provider_display = (
                    profile.hospital.name
                    if profile and getattr(profile, "hospital", None)
                    else ((getattr(profile, "organisation_name", None) or "").strip() if profile else claim.provider.username)
                )
                return render(
                    request,
                    "patient/verify.html",
                    {
                        "claim": claim,
                        "provider_display": provider_display,
                        "invalid": False,
                        "is_expired": is_expired,
                        "is_used": is_used,
                        "ipm_share": snapshot.get("ipm_share"),
                        "patient_share": snapshot.get("patient_share"),
                        "coverage_percent": snapshot.get("coverage_percent"),
                        "dispute_reason_error": "Veuillez indiquer la raison de votre contestation.",
                        "dispute_reason_value": request.POST.get("dispute_reason", ""),
                    },
                )
            claim.dispute_reason = dispute_reason
            claim.save(update_fields=["dispute_reason"])
            try:
                ClaimStateMachine.patient_dispute(claim)
            except ClaimTransitionError:
                return render(request, "patient/verify.html", {"claim": claim, "invalid": True, "link_used_outcome": "invalid"})
            return render(request, "patient/verify.html", {"claim": claim, "done": "disputed"})

    snapshot = claim.snapshot_json or {}
    profile = getattr(claim.provider, "staff_profile", None)
    if profile and getattr(profile, "hospital", None):
        provider_display = profile.hospital.name
    elif profile and (getattr(profile, "organisation_name", None) or "").strip():
        provider_display = (profile.organisation_name or "").strip()
    else:
        provider_display = claim.provider.username
    invalid = claim.status != ClaimStatus.LOCKED or is_expired or is_used
    return render(
        request,
        "patient/verify.html",
        {
            "claim": claim,
            "provider_display": provider_display,
            "invalid": invalid,
            "link_used_outcome": _link_used_outcome() if invalid else None,
            "is_expired": is_expired,
            "is_used": is_used,
            "ipm_share": snapshot.get("ipm_share"),
            "patient_share": snapshot.get("patient_share"),
            "coverage_percent": snapshot.get("coverage_percent"),
        },
    )
