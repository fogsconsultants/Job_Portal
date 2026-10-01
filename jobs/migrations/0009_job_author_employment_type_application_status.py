# Generated manually because the local Python executable is unavailable in this workspace.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0008_application_unique_constraint"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="jobs",
            name="author",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posted_jobs", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="jobs",
            name="employment_type",
            field=models.CharField(default="Full-time", max_length=30),
        ),
        migrations.AddField(
            model_name="applications",
            name="status",
            field=models.CharField(default="Submitted", max_length=20),
        ),
    ]
