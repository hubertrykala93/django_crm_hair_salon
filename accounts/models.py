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
                basic_info = ProfileBasicInformation.objects.create()
                contact_info = ProfileContactInformation.objects.create()
                employment_info = ProfileEmploymentInformation.objects.create()
                job_position = JobPosition.objects.create()
                employment_status = EmploymentStatus.objects.create()
                contract = Contract.objects.create()

                profile_image = ProfileImage.objects.create()
                basic_info.profile_image = profile_image
                basic_info.save()

                profile.basicinformation = basic_info
                profile.contactinformation = contact_info
                profile.employmentinformation = employment_info
                profile.employmentinformation.job_position = job_position
                profile.employmentinformation.employment_status = employment_status
                profile.employmentinformation.contract = contract
                employment_info.save()

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


class ProfileBasicInformation(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profile_image = models.OneToOneField(to=ProfileImage, on_delete=models.CASCADE, null=True)
    biography = models.TextField(max_length=10000, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Profile Basic Information"
        verbose_name_plural = "Profile Basic Information"

    def __str__(self):
        return str(self.pk)


class ProfileContactInformation(models.Model):
    phone_number = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    house_number = models.CharField(max_length=10, null=True)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "Profile Contact Information"
        verbose_name_plural = "Profile Contact Information"

    def __str__(self):
        return str(self.pk)


class JobPosition(models.Model):
    name = models.CharField(default="Not Defined", max_length=200)

    class Meta:
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"

    def __str__(self):
        return str(self.id)

    # positions = ["Owner","Manager","Receptionist","Hairstylist","Assistant","Barber"]


class EmploymentStatus(models.Model):
    name = models.CharField(default="Inactive", max_length=100)

    class Meta:
        verbose_name = "Employment Status"
        verbose_name_plural = "Employment Statuses"

    def __str__(self):
        return str(self.id)

    # statuses = ["Active", "Inactive", "On Leave"]


class Contract(models.Model):
    name = models.CharField(default="Not Defined", max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    work_hours_per_week = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.id)
    
    # contracts = [
    #     "Employment Contract",
    #     "Contract of Mandate",
    #     "Contract for Specific Work",
    #     "B2B",
    #     "Agency Contract",
    #     "Internship Contract",
    #     "Temporary Employment Contract"
    # ]


class ProfileEmploymentInformation(models.Model):
    job_position = models.OneToOneField(to=JobPosition, on_delete=models.CASCADE, null=True, blank=True)
    employment_status = models.OneToOneField(to=EmploymentStatus, on_delete=models.CASCADE, null=True, blank=True)
    contract = models.OneToOneField(to=Contract, on_delete=models.CASCADE, null=True, blank=True)

    # benefits

    class Meta:
        verbose_name = "Profile Employment Information"
        verbose_name_plural = "Profile Employment Information"

    def __str__(self):
        return str(self.pk)


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    basicinformation = models.OneToOneField(to=ProfileBasicInformation, on_delete=models.CASCADE, null=True)
    contactinformation = models.OneToOneField(to=ProfileContactInformation, on_delete=models.CASCADE, null=True)
    employmentinformation = models.OneToOneField(to=ProfileEmploymentInformation, on_delete=models.CASCADE, null=True)

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
        print(profile.basicinformation)
        print(profile.basicinformation.profile_image)

        if hasattr(profile, "basicinformation"):
            print("Profile has Attribute BasicInformation.")
            if hasattr(profile.basicinformation, "profile_image"):
                print("BasicInformation has Attribute ProfileImage.")
                if profile.basicinformation.profile_image:
                    print("Profile BasicInformation ProfileImage & Profile BasicInformation ProfileImage Image")
                    image_path = profile.basicinformation.profile_image.image.path

                    if "default_profile_image.png" not in image_path:
                        if os.path.isfile(path=image_path):
                            os.remove(path=image_path)

                    print("Profile Image Deleting...")
                    profile.basicinformation.profile_image.delete()
                    print("Profile Image Delete.")

                print("Profile Basic Information Deleting...")
                profile.basicinformation.delete()
                print("Profile Basic Information Delete.")

            if hasattr(profile, "contactinformation"):
                print("Profile has Attribute ContactInformation.")
                if profile.contactinformation:
                    print("Profile ContactInformation Deleting...")
                    profile.contactinformation.delete()
                    print("Profile ContactInformation Deleted.")

            if hasattr(profile, "employmentinformation"):
                print("Profile has Attribute EmploymentInformation.")
                if profile.employmentinformation:
                    if hasattr(profile.employmentinformation, "job_position"):
                        print("Job Position Deleting...")
                        profile.employmentinformation.job_position.delete()
                        print("Job Position Deleted.")

                    if hasattr(profile.employmentinformation, "employment_status"):
                        print("Employment Status Deleting...")
                        profile.employmentinformation.employment_status.delete()
                        print("Employment Status Deleted.")

                    if hasattr(profile.employmentinformation, "contract"):
                        print("Contract Deleting...")
                        profile.employmentinformation.contract.delete()
                        print("Contract Deleted.")

                    print("Profile EmploymentInformation Deleting...")
                    profile.employmentinformation.delete()
                    print("Profile EmploymentInformation Deleted.")

        print("Profile Deleting...")
        profile.delete()
        print("Profile Deleted.")
