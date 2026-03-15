# Step 3: Remove old ipm FK from CoverageRule and add final unique constraint

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("claims", "0004_populate_coverage_plans"),
    ]

    operations = [
        # Remove old ipm FK from CoverageRule
        migrations.RemoveField(
            model_name="coveragerule",
            name="ipm",
        ),
        # Add unique constraint on (coverage_plan, category)
        migrations.AddConstraint(
            model_name="coveragerule",
            constraint=models.UniqueConstraint(fields=("coverage_plan", "category"), name="unique_coverage_per_plan_category"),
        ),
    ]
