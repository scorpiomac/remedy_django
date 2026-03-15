"""
Envoi d'emails avec enregistrement dans EmailLog (statut, contenu) pour suivi et renvoi.
"""
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import EmailLog

logger = logging.getLogger(__name__)


def send_and_log_email(
    to_list,
    subject,
    body_plain,
    from_email=None,
    body_html=None,
    email_type="",
    related_ref="",
):
    """
    Envoie un email et crée une entrée EmailLog (succès ou échec).
    to_list: liste d'adresses
    from_email: si None, utilise settings.DEFAULT_FROM_EMAIL
    Retourne l'instance EmailLog créée.
    """
    if not to_list:
        return None
    to_list = [e.strip() for e in to_list if e and str(e).strip()]
    if not to_list:
        return None
    from_email = from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "")
    log_kwargs = {
        "to_emails": ",".join(to_list),
        "from_email": from_email,
        "subject": subject[:500],
        "body_plain": (body_plain or "")[:10000],
        "body_html": (body_html or "")[:50000],
        "email_type": email_type[:50] if email_type else "",
        "related_ref": related_ref[:255] if related_ref else "",
    }
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=body_plain or "",
            from_email=from_email,
            to=to_list,
        )
        if body_html:
            msg.attach_alternative(body_html, "text/html")
        msg.send(fail_silently=False)
        log_kwargs["status"] = "sent"
        log_kwargs["error_message"] = ""
    except Exception as e:
        logger.exception("Envoi email échoué: %s", e)
        log_kwargs["status"] = "failed"
        log_kwargs["error_message"] = str(e)[:2000]
    return EmailLog.objects.create(**log_kwargs)


def resend_email(email_log):
    """
    Renvoie un email à partir d'un EmailLog (même contenu).
    Retourne le nouveau EmailLog (sent ou failed).
    """
    to_list = email_log.get_to_list()
    if not to_list:
        return None
    return send_and_log_email(
        to_list=to_list,
        subject=email_log.subject,
        body_plain=email_log.body_plain,
        from_email=email_log.from_email,
        body_html=email_log.body_html or None,
        email_type=email_log.email_type or "resend",
        related_ref=f"resend_of:{email_log.pk}",
    )
