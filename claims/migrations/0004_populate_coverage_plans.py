# Step 2: Data migration — create default plans, migrate existing rules and patients

from django.db import migrations


def forward(apps, schema_editor):
    IPM = apps.get_model("claims", "IPM")
    CoveragePlan = apps.get_model("claims", "CoveragePlan")
    CoverageRule = apps.get_model("claims", "CoverageRule")
    Patient = apps.get_model("claims", "Patient")

    for ipm in IPM.objects.all():
        plan, _ = CoveragePlan.objects.get_or_create(
            ipm=ipm,
            name="Formule Standard",
            defaults={"is_active": True},
        )
        # Migrate coverage rules: set coverage_plan from old ipm FK
        CoverageRule.objects.filter(coverage_plan__isnull=True, ipm_id=ipm.pk).update(coverage_plan=plan)
        # Assign patients of this IPM to the default plan
        Patient.objects.filter(ipm=ipm, coverage_plan__isnull=True).update(coverage_plan=plan)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("claims", "0003_coverage_plan_refactor"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
