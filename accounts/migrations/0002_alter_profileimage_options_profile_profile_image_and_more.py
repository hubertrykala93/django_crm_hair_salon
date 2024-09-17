# Generated by Django 4.2.16 on 2024-09-13 21:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profileimage",
            options={
                "verbose_name": "Profile Image",
                "verbose_name_plural": "Profile Images",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_image",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.profileimage",
            ),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="alt",
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="format",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="height",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="image",
            field=models.ImageField(
                default="accounts/profile_images/default_profile_image.png",
                null=True,
                upload_to="accounts/profile_images",
            ),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="size",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="width",
            field=models.IntegerField(null=True),
        ),
    ]