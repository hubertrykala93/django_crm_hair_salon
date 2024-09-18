from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.timezone import now
from uuid import uuid4
import os
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import random as rnd


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address.")

        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(default=now)
    username = models.CharField(max_length=1000, default=uuid4, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        if self.pk:
            profile, created = Profile.objects.get_or_create(user=self)

            if created:
                profile_image = ProfileImage.objects.create()
                profile.profile_image = profile_image

                profile.save()


class OneTimePassword(models.Model):
    created_at = models.DateTimeField(default=now)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    password = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name = "One Time Password"
        verbose_name_plural = "One Time Passwords"

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = ''.join([str(rnd.randint(a=0, b=9)) for _ in range(6)])

        super(OneTimePassword, self).save(*args, **kwargs)


class ProfileImage(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        default="accounts/profile_images/default_profile_image.png",
        upload_to="accounts/profile_images",
        null=True
    )
    size = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    alt = models.CharField(max_length=1000, null=True)

    class Meta:
        verbose_name = "Profile Image"
        verbose_name_plural = "Profile Images"

    def __str__(self):
        return f"{self.pk}"

    def save(self, *args, **kwargs):
        if self.pk:
            super(ProfileImage, self).save(*args, **kwargs)

            instance = ProfileImage.objects.get(id=self.id)

            self._resize_image()
            self._save_attributes(instance=instance)

            super(ProfileImage, self).save(*args, **kwargs)

        else:
            self._resize_image()
            self._save_attributes()

            super(ProfileImage, self).save(*args, **kwargs)

    def _resize_image(self):
        image = Image.open(fp=self.image.path)

        if image.mode == "RGBA":
            image = image.convert(mode="RGB")

        image.thumbnail(size=(300, 300))
        image.save(fp=self.image.path)

        return image

    def _save_attributes(self, instance=None):
        image = self._resize_image()

        if "default_profile_image.png" in self.image.path:
            self.alt = "Default profile picture"

        if instance:
            self.alt = f"User profile picture"

        self.size = os.path.getsize(filename=self.image.path)
        self.width, self.height = image.width, image.height
        self.format = image.format


class Profile(models.Model):
    USER_TYPES = (
        ("Owner", "Owner"),
        ("Manager", "Manager"),
        ("Receptionist", "Receptionist"),
        ("Hairstylist", "Hairstylist"),
        ("Assistant", "Assistant"),
        ("Barber", "Barber"),
        ("Not Defined", "Not Defined"),
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profileimage = models.OneToOneField(to=ProfileImage, on_delete=models.SET_NULL, null=True)
    usertype = models.CharField(
        default="Not Defined",
        max_length=200,
        choices=USER_TYPES,
    )
    dateofbirth = models.DateField(null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    housenumber = models.CharField(max_length=10, null=True)
    apartmentnumber = models.CharField(max_length=10, null=True, blank=True)
    biography = models.TextField(max_length=10000, null=True)
    dateofemployment = models.DateField(null=True, blank=True)
    employmentstatus = models.CharField(
        max_length=50,
        choices=(
            ("Active", "Active"),
            ("On Leave", "On Leave"),
            ("Inactive", "Inactive"),
        ),
        default="Active",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.pk}"


@receiver(signal=pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile

    except Profile.DoesNotExist:
        pass

    if instance.profile:
        profile = instance.profile

        if hasattr(profile, "profile_image"):
            if profile.profile_image and profile.profile_image.image:
                image_path = profile.profile_image.image.path

                if "default_profile_image.png" not in image_path:
                    if os.path.isfile(path=image_path):
                        os.remove(path=image_path)

                profile.profile_image.delete()

        profile.delete()
