# Generated by Django 5.1 on 2024-09-23 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_profilecontactinformation_postalcode"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profilebasicinformation",
            old_name="dateofbirth",
            new_name="date_of_birth",
        ),
        migrations.RenameField(
            model_name="profilebasicinformation",
            old_name="profileimage",
            new_name="profile_image",
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="contractduration",
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="contractenddate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="contractstartdate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="contracttype",
            field=models.CharField(
                choices=[
                    ("Employment Contract", "Employment Contract"),
                    ("Contract of Mandate", "Contract of Mandate"),
                    ("Contract for Specific Work", "Contract for Specific Work"),
                    ("B2B", "B2B"),
                    ("Agency Contract", "Agency Contract"),
                    ("Internship Contract", "Internship Contract"),
                    ("Temporary Employment Contract", "Temporary Employment Contract"),
                ],
                default="Not Defined",
                max_length=200,
            ),
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="salary",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="profileemploymentinformation",
            name="work_hours_per_week",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profileemploymentinformation",
            name="employmentstatus",
            field=models.CharField(
                choices=[
                    ("Active", "Active"),
                    ("On Leave", "On Leave"),
                    ("Inactive", "Inactive"),
                ],
                default="Inactive",
                max_length=50,
            ),
        ),
    ]
