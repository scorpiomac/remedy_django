import secrets
from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Claim, ClaimAuditLog, ClaimStatus, CoverageRule


class ClaimTransitionError(Exception):
    pass


class ClaimStateMachine:
    @staticmethod
    def _audit(claim, actor, event, notes=""):
        ClaimAuditLog.objects.create(claim=claim, actor=actor, event=event, notes=notes)

    @staticmethod
    def _coverage_snapshot(claim):
        """Build coverage snapshot using patient's CoveragePlan instead of IPM directly."""
        plan = claim.patient.coverage_plan
        rule = None
        if plan:
            rule = CoverageRule.objects.filter(
                coverage_plan=plan, category=claim.category, is_active=True
            ).first()
        coverage_percent = rule.coverage_percent if rule else Decimal("0.00")
        ipm_share = (claim.total_amount * coverage_percent / Decimal("100.00")).quantize(Decimal("0.01"))
        patient_share = (claim.total_amount - ipm_share).quantize(Decimal("0.01"))
        return {
            "claim_id": claim.id,
            "locked_at": timezone.now().isoformat(),
            "ipm": claim.patient.ipm.name,
            "formule": plan.name if plan else "",
            "patient": claim.patient.full_name,
            "category": claim.category.name,
            "total_amount": str(claim.total_amount),
            "coverage_percent": str(coverage_percent),
            "ipm_share": str(ipm_share),
            "patient_share": str(patient_share),
            "medicine_names": claim.medicine_names,
        }

    @staticmethod
    def _detect_tampering(claim):
        snap = claim.snapshot_json or {}
        if not snap:
            return True
        expected = {
            "patient": claim.patient.full_name,
            "category": claim.category.name,
            "total_amount": str(claim.total_amount),
            "medicine_names": claim.medicine_names or "",
        }
        actual = {
            "patient": snap.get("patient"),
            "category": snap.get("category"),
            "total_amount": str(snap.get("total_amount")),
            "medicine_names": snap.get("medicine_names") or "",
        }
        return expected != actual

    @classmethod
    @transaction.atomic
    def submit(cls, claim, actor):
        if claim.status != ClaimStatus.DRAFT:
            raise ClaimTransitionError("Only DRAFT can transition to SUBMITTED.")
        if not claim.documents.exists():
            raise ClaimTransitionError("Au moins un document justificatif est requis avant soumission.")
        claim.status = ClaimStatus.SUBMITTED
        claim.submitted_at = timezone.now()
        claim.save(update_fields=["status", "submitted_at", "updated_at"])
        cls._audit(claim, actor, "CLAIM_SUBMITTED", "Claim submitted by provider")
        # Verrouillage automatique : génération du lien patient sans action admin.
        cls.lock(claim, actor)
        return claim

    @classmethod
    @transaction.atomic
    def lock(cls, claim, actor):
        if claim.status != ClaimStatus.SUBMITTED:
            raise ClaimTransitionError("Only SUBMITTED can transition to LOCKED.")
        claim.snapshot_json = cls._coverage_snapshot(claim)
        claim.status = ClaimStatus.LOCKED
        claim.locked_at = timezone.now()
        claim.patient_token = secrets.token_hex(32)
        claim.token_expires_at = timezone.now() + timedelta(days=3)
        claim.save(
            update_fields=[
                "snapshot_json",
                "status",
                "locked_at",
                "patient_token",
                "token_expires_at",
                "updated_at",
            ]
        )
        cls._audit(claim, actor, "CLAIM_LOCKED", "Snapshot generated and token issued")
        return claim

    @classmethod
    @transaction.atomic
    def patient_confirm(cls, claim):
        if claim.status != ClaimStatus.LOCKED:
            raise ClaimTransitionError("Only LOCKED claim can be patient-confirmed.")
        if cls._detect_tampering(claim):
            claim.status = ClaimStatus.BLOCKED
            claim.block_reason = "Fraud suspicion: snapshot mismatch"
            claim.token_used_at = timezone.now()
            claim.save(update_fields=["status", "block_reason", "token_used_at", "updated_at"])
            cls._audit(claim, None, "CLAIM_BLOCKED", "Auto blocked due to snapshot mismatch")
            return claim

        claim.status = ClaimStatus.PATIENT_CONFIRMED
        claim.token_used_at = timezone.now()
        claim.save(update_fields=["status", "token_used_at", "updated_at"])
        cls._audit(claim, None, "PATIENT_CONFIRMED", "Patient confirmed snapshot")

        claim.status = ClaimStatus.READY_FOR_PAYMENT
        claim.save(update_fields=["status", "updated_at"])
        cls._audit(claim, None, "READY_FOR_PAYMENT", "Claim ready for payment")
        return claim

    @classmethod
    @transaction.atomic
    def patient_dispute(cls, claim):
        if claim.status != ClaimStatus.LOCKED:
            raise ClaimTransitionError("Only LOCKED claim can be disputed.")
        claim.status = ClaimStatus.DISPUTED
        claim.token_used_at = timezone.now()
        claim.save(update_fields=["status", "token_used_at", "updated_at"])
        cls._audit(claim, None, "PATIENT_DISPUTED", "Patient disputed snapshot")

        claim.status = ClaimStatus.BLOCKED
        reason = (getattr(claim, "dispute_reason", None) or "").strip() or "Patient dispute after lock"
        claim.block_reason = reason[:255] if len(reason) > 255 else reason
        claim.save(update_fields=["status", "block_reason", "updated_at"])
        cls._audit(claim, None, "CLAIM_BLOCKED", "Blocked after patient dispute")
        return claim
