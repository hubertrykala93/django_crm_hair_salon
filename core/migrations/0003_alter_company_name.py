# Generated by Django 5.1 on 2024-10-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_company_options_company_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
