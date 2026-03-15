# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("claims", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="claim",
            name="care_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="claim",
            name="invoice_number",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="claimdocument",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("ORDONNANCE", "Ordonnance"),
                    ("FACTURE", "Facture"),
                    ("BON_PRISE_EN_CHARGE", "Bon de prise en charge"),
                    ("RESULTAT_LABO", "Résultat laboratoire"),
                    ("AUTRE", "Autre"),
                ],
                default="AUTRE",
                max_length=25,
            ),
        ),
    ]
