from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0007_rename_application_applications"),
    ]

    operations = [
        migrations.RunSQL(
            "DELETE FROM jobs_applications WHERE id NOT IN (SELECT MIN(id) FROM jobs_applications GROUP BY job_id, user_id)",
            migrations.RunSQL.noop,
        ),
        migrations.AddConstraint(
            model_name="applications",
            constraint=models.UniqueConstraint(fields=("job", "user"), name="unique_job_application"),
        ),
    ]
