from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.timezone import now
from uuid import uuid4
import os
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import random as rnd
from contracts.models import Contract, Benefit, EmploymentStatus
from payments.models import BankTransfer, PrepaidTransfer, PayPalTransfer, CryptoTransfer, CryptoCurrency
import secrets
import string


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
        return str(self.email)

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(seq=alphabet) for _ in range(12))

        return password

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        if self.pk:
            profile, created = Profile.objects.get_or_create(user=self)

            if created:
                # Creating Basic Information for Profile
                basic_info = ProfileBasicInformation.objects.create()
                profile.basic_information = basic_info

                # Creating Contact Information for Profile
                contact_info = ProfileContactInformation.objects.create()
                profile.contact_information = contact_info

                # Creating Contract for Profile
                contract = Contract.objects.create()
                profile.contract = contract

                # Creating Profile Image for Basic Information
                profile_image = ProfileImage.objects.create()
                basic_info.profile_image = profile_image

                # Saving Basic Information with Profile Image
                basic_info.save()

                # Creating Employment Status for Contract
                if not EmploymentStatus.objects.filter(name="Active").exists():
                    status = EmploymentStatus.objects.create(name="Active")
                    status.save()

                else:
                    contract.status = EmploymentStatus.objects.get(name="Active")

                # Creating and Saving Benefits for Contract
                benefits = Benefit.objects.create()
                contract.benefits = benefits
                contract.save()

                # Creating BankTransfer
                bank_transfer = BankTransfer.objects.create(name=f"Bank Transfer for {self.username}", user=self)
                bank_transfer.save()

                # Creating PrepaidTransfer
                prepaid_transfer = PrepaidTransfer.objects.create(name=f"Prepaid Transfer for {self.username}",
                                                                  user=self)
                prepaid_transfer.save()

                # Creating PayPalTransfer
                paypal_transfer = PayPalTransfer.objects.create(name=f"PayPal Transfer for {self.username}", user=self)
                paypal_transfer.save()

                # Creating CryptoTransfer
                crypto_transfer = CryptoTransfer.objects.create(name=f"Crypto Transfer for {self.username}", user=self)

                if not CryptoCurrency.objects.filter(name="Bitcoin").exists():
                    cryptocurrency = CryptoCurrency.objects.create(name="Bitcoin", code="BTC")
                    cryptocurrency.save()

                else:
                    crypto_transfer.cryptocurrency = CryptoCurrency.objects.get(name="Bitcoin")
                    crypto_transfer.save()

                # Saving Profile with Basic Information, Contact Information, Employment Information
                profile.save()


class OneTimePassword(models.Model):
    created_at = models.DateTimeField(default=now)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    password = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name = "One Time Password"
        verbose_name_plural = "One Time Passwords"

    def __str__(self):
        return str(self.pk)

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
        return str(self.pk)

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


class ProfileBasicInformation(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profile_image = models.OneToOneField(to=ProfileImage, on_delete=models.SET_NULL, null=True)
    biography = models.TextField(max_length=10000, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Basic Information"
        verbose_name_plural = "Basic Information"

    def __str__(self):
        return str(self.pk)


class ProfileContactInformation(models.Model):
    phone_number = models.CharField(max_length=20, null=True, unique=True)
    country = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    house_number = models.CharField(max_length=10, null=True)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return str(self.pk)


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    basic_information = models.OneToOneField(to=ProfileBasicInformation, on_delete=models.CASCADE, null=True)
    contact_information = models.OneToOneField(to=ProfileContactInformation, on_delete=models.CASCADE, null=True)
    contract = models.OneToOneField(to=Contract, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.pk)


@receiver(signal=pre_delete, sender=User)
def delete_instances(sender, instance, **kwargs):
    try:
        profile = instance.profile

    except Profile.DoesNotExist:
        pass

    if hasattr(instance, "profile"):
        if hasattr(instance.profile, "basic_information"):
            if hasattr(instance.profile.basic_information, "profile_image"):
                if instance.profile.basic_information.profile_image is not None:
                    image_path = instance.profile.basic_information.profile_image.image.path

                    if "default_profile_image" not in image_path:
                        if os.path.isfile(path=image_path):
                            os.remove(path=image_path)

                    instance.profile.basic_information.profile_image.delete()

            if getattr(instance.profile, "basic_information"):
                instance.profile.basic_information.delete()

        if hasattr(instance.profile, "contact_information"):
            if getattr(instance.profile, "contact_information"):
                instance.profile.contact_information.delete()

        if hasattr(instance.profile, "contract"):
            if hasattr(instance.profile.contract, "benefits"):
                if getattr(instance.profile.contract, "benefits"):
                    instance.profile.contract.benefits.delete()

            if getattr(instance.profile, "contract"):
                instance.profile.contract.delete()

        if getattr(instance, "profile"):
            instance.profile.delete()
