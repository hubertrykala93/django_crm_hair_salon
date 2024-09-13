# Generated by Django 4.2.16 on 2024-09-13 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_profile_dateofbirth"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "Profile", "verbose_name_plural": "Profiles"},
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="accounts.profileimage",
            ),
        ),
    ]
