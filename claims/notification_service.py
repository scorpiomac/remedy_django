"""
Envoi des notifications (lien de validation) au patient après verrouillage du dossier.
Log chaque envoi avec statut (SENT/FAILED) et message d'erreur ; permet le renvoi depuis la fiche dossier.
"""
import json
import logging
import urllib.error
import urllib.request
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.urls import reverse

from core.models import EmailLog
from .models import NotificationChannel, NotificationChannelConfig, NotificationLog

logger = logging.getLogger(__name__)


def replace_placeholders(text, context):
    if not text:
        return text
    for k, v in context.items():
        text = text.replace("{{ " + k + " }}", str(v)).replace("{{" + k + "}}", str(v))
    return text


def _build_context(claim, request):
    verify_url = request.build_absolute_uri(
        reverse("patient_verify_public", args=[claim.patient_token])
    ) if claim.patient_token else ""
    return {
        "patient_name": claim.patient.full_name,
        "verify_link": verify_url,
        "claim_id": str(claim.id),
    }


def _log_notification(claim, channel, target, status, error_message=""):
    return NotificationLog.objects.create(
        claim=claim,
        channel=channel,
        target=target[:255],
        status=status,
        error_message=error_message[:2000] if error_message else "",
    )


def send_claim_notification_email(claim, request):
    """Envoie l'email au patient avec le lien de validation. Log SENT ou FAILED."""
    config = NotificationChannelConfig.objects.filter(
        channel=NotificationChannel.EMAIL.value, is_active=True
    ).first()
    if not config:
        return
    cfg = config.config or {}
    patient = claim.patient
    to_email = (patient.email or "").strip()
    if not to_email or "@" not in to_email:
        _log_notification(
            claim, NotificationChannel.EMAIL.value, to_email or "(aucun email)",
            "FAILED", "Patient sans adresse email valide.",
        )
        return
    ctx = _build_context(claim, request)
    subject = replace_placeholders(cfg.get("subject_template") or "[REMEDY] Votre réclamation à valider", ctx)
    body = replace_placeholders(cfg.get("body_template") or "Bonjour {{ patient_name }}, cliquez ici pour valider : {{ verify_link }}", ctx)
    from_email = cfg.get("from_email") or "noreply@remedy.local"
    related_ref = f"claim:{claim.id}"
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
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email],
            connection=backend,
        )
        msg.send()
        _log_notification(claim, NotificationChannel.EMAIL.value, to_email, "SENT")
        EmailLog.objects.create(
            to_emails=to_email,
            from_email=from_email,
            subject=subject,
            body_plain=body,
            body_html="",
            status="sent",
            error_message="",
            email_type="claim_notification",
            related_ref=related_ref,
        )
    except Exception as e:
        err = str(e)
        logger.exception("Envoi email réclamation %s échoué", claim.id)
        _log_notification(claim, NotificationChannel.EMAIL.value, to_email, "FAILED", err)
        EmailLog.objects.create(
            to_emails=to_email,
            from_email=from_email,
            subject=subject,
            body_plain=body,
            body_html="",
            status="failed",
            error_message=err[:2000],
            email_type="claim_notification",
            related_ref=related_ref,
        )


def send_claim_notification_sms(claim, request):
    """Envoie le SMS au patient (API configurée). Log SENT ou FAILED."""
    config = NotificationChannelConfig.objects.filter(
        channel=NotificationChannel.SMS.value, is_active=True
    ).first()
    if not config:
        return
    cfg = config.config or {}
    api_url = (cfg.get("api_url") or "").strip()
    api_key = (cfg.get("api_key") or "").strip()
    patient = claim.patient
    to_phone = (patient.phone or "").strip()
    if not to_phone:
        _log_notification(
            claim, NotificationChannel.SMS.value, "(aucun téléphone)",
            "FAILED", "Patient sans numéro de téléphone.",
        )
        return
    if not api_url:
        _log_notification(
            claim, NotificationChannel.SMS.value, to_phone,
            "FAILED", "Canal SMS actif mais URL API non configurée.",
        )
        return
    ctx = _build_context(claim, request)
    body = replace_placeholders(cfg.get("body_template") or "REMEDY: validez votre réclamation {{ claim_id }} : {{ verify_link }}", ctx)
    try:
        payload = {
            "phone": to_phone,
            "message": body,
            "sender": (cfg.get("sender") or "REMEDY")[:11],
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, method="POST", headers={"Content-Type": "application/json"})
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status in (200, 201):
                _log_notification(claim, NotificationChannel.SMS.value, to_phone, "SENT")
            else:
                _log_notification(
                    claim, NotificationChannel.SMS.value, to_phone,
                    "FAILED", f"API SMS: {resp.status}",
                )
    except urllib.error.HTTPError as e:
        body_read = e.read().decode("utf-8", errors="replace")[:500]
        _log_notification(
            claim, NotificationChannel.SMS.value, to_phone,
            "FAILED", f"API SMS: {e.code} - {body_read}",
        )
    except Exception as e:
        err = str(e)
        logger.exception("Envoi SMS réclamation %s échoué", claim.id)
        _log_notification(claim, NotificationChannel.SMS.value, to_phone, "FAILED", err)


def send_claim_notification_whatsapp(claim, request):
    """Envoie le message WhatsApp au patient (API configurée). Log SENT ou FAILED."""
    config = NotificationChannelConfig.objects.filter(
        channel=NotificationChannel.WHATSAPP.value, is_active=True
    ).first()
    if not config:
        return
    cfg = config.config or {}
    api_url = (cfg.get("api_url") or "").strip()
    api_key = (cfg.get("api_key") or "").strip()
    patient = claim.patient
    to_phone = (patient.phone or "").strip()
    if not to_phone:
        _log_notification(
            claim, NotificationChannel.WHATSAPP.value, "(aucun téléphone)",
            "FAILED", "Patient sans numéro de téléphone.",
        )
        return
    if not api_url:
        _log_notification(
            claim, NotificationChannel.WHATSAPP.value, to_phone,
            "FAILED", "Canal WhatsApp actif mais URL API non configurée.",
        )
        return
    ctx = _build_context(claim, request)
    body = replace_placeholders(cfg.get("body_template") or "REMEDY: validez votre réclamation {{ claim_id }} : {{ verify_link }}", ctx)
    try:
        payload = {"phone": to_phone, "message": body}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, method="POST", headers={"Content-Type": "application/json"})
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status in (200, 201):
                _log_notification(claim, NotificationChannel.WHATSAPP.value, to_phone, "SENT")
            else:
                _log_notification(
                    claim, NotificationChannel.WHATSAPP.value, to_phone,
                    "FAILED", f"API WhatsApp: {resp.status}",
                )
    except urllib.error.HTTPError as e:
        body_read = e.read().decode("utf-8", errors="replace")[:500]
        _log_notification(
            claim, NotificationChannel.WHATSAPP.value, to_phone,
            "FAILED", f"API WhatsApp: {e.code} - {body_read}",
        )
    except Exception as e:
        err = str(e)
        logger.exception("Envoi WhatsApp réclamation %s échoué", claim.id)
        _log_notification(claim, NotificationChannel.WHATSAPP.value, to_phone, "FAILED", err)


def send_claim_notifications(claim, request, channels=None):
    """
    Envoie les notifications (lien de validation) pour tous les canaux actifs, ou ceux indiqués.
    channels: liste optionnelle de NotificationChannel.value (ex. ["EMAIL"]). Si None, tous les actifs.
    """
    if not claim.patient_token or claim.status != "LOCKED":
        return
    if channels is None:
        channels = [
            c.channel for c in NotificationChannelConfig.objects.filter(is_active=True)
        ]
    if NotificationChannel.EMAIL.value in channels:
        send_claim_notification_email(claim, request)
    if NotificationChannel.SMS.value in channels:
        send_claim_notification_sms(claim, request)
    if NotificationChannel.WHATSAPP.value in channels:
        send_claim_notification_whatsapp(claim, request)
