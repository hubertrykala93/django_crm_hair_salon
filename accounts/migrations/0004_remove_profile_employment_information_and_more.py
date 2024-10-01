# Generated by Django 5.1 on 2024-10-01 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_profileemploymentinformation_job_position"),
        ("contracts", "0006_contract_job_position"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="employment_information",),
        migrations.AddField(
            model_name="profile",
            name="contract",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contracts.contract",
            ),
        ),
        migrations.DeleteModel(name="ProfileEmploymentInformation",),
    ]
