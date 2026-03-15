# Step 1: Add new models and fields, keep old ipm FK for data migration

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("claims", "0002_add_care_date_invoice_document_type"),
    ]

    operations = [
        # Create CoveragePlan
        migrations.CreateModel(
            name="CoveragePlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Nom de la formule (ex: Formule A 80%)", max_length=150)),
                ("annual_ceiling", models.DecimalField(blank=True, decimal_places=2, help_text="Plafond annuel en FCFA (laisser vide = illimite)", max_digits=12, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("ipm", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="plans", to="claims.ipm")),
            ],
        ),
        migrations.AddConstraint(
            model_name="coverageplan",
            constraint=models.UniqueConstraint(fields=("ipm", "name"), name="unique_plan_per_ipm"),
        ),
        # Add beneficiary_type to Patient
        migrations.AddField(
            model_name="patient",
            name="beneficiary_type",
            field=models.CharField(choices=[("TITULAIRE", "Titulaire (adherent principal)"), ("CONJOINT", "Conjoint(e)"), ("ENFANT", "Enfant"), ("AYANT_DROIT", "Ayant droit")], default="TITULAIRE", max_length=20),
        ),
        # Add coverage_plan FK to Patient (nullable)
        migrations.AddField(
            model_name="patient",
            name="coverage_plan",
            field=models.ForeignKey(blank=True, help_text="Formule de couverture du patient", null=True, on_delete=django.db.models.deletion.PROTECT, related_name="patients", to="claims.coverageplan"),
        ),
        # Add coverage_plan FK to CoverageRule (nullable) — keep old ipm FK for now
        migrations.RemoveConstraint(
            model_name="coveragerule",
            name="unique_coverage_per_ipm_category",
        ),
        migrations.AddField(
            model_name="coveragerule",
            name="coverage_plan",
            field=models.ForeignKey(blank=True, help_text="Formule de couverture", null=True, on_delete=django.db.models.deletion.PROTECT, related_name="rules", to="claims.coverageplan"),
        ),
    ]
