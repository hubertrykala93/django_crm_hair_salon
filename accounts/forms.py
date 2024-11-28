from django import forms
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password
from PIL import Image
from datetime import date, datetime


class AdminRegisterForm(forms.ModelForm):
    email = forms.CharField(
        help_text="Enter e-mail address.",
        label="Email",
        required=True
    )
    password = forms.CharField(
        help_text="Enter password.",
        label="Password", required=True,
        widget=forms.PasswordInput
    )
    is_active = forms.BooleanField(
        help_text="Check if the user should be active.",
        required=False,
    )
    is_staff = forms.BooleanField(
        help_text="Check if the user should be staff.",
        required=False
    )
    is_superuser = forms.BooleanField(
        help_text="Check if the user should be a superuser.",
        required=False
    )

    class Meta:
        model = User
        exclude = [
            "groups",
            # "user_permissions",
        ]

    def save(self, commit=True):
        user = super(AdminRegisterForm, self).save(commit=False)

        if self.cleaned_data["password"]:
            user.password = make_password(password=self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class AdminOneTimePasswordForm(forms.ModelForm):
    class Meta:
        model = OneTimePassword
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminOneTimePasswordForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


class AdminProfileBasicInformationForm(forms.ModelForm):
    firstname = forms.CharField(help_text="Enter your first name.", label="First Name", required=True)
    lastname = forms.CharField(help_text="Enter your last name.", label="Last Name", required=True)
    date_of_birth = forms.DateField(help_text="Enter your date of birth.", label="Date of Birth", required=True)
    biography = forms.CharField(help_text="Write a short biography.", label="Biography", required=False,
                                widget=forms.Textarea)

    class Meta:
        model = ProfileBasicInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileBasicInformationForm, self).__init__(*args, **kwargs)

        self.fields["profile_image"].help_text = "Select the profile image."
        self.fields["profile_image"].label = "Profile Image"
        self.fields["profile_image"].required = True


class AdminProfileContactInformationForm(forms.ModelForm):
    phone_number = forms.CharField(help_text="Enter your phone number.", label="Phone Number", required=True)
    country = forms.CharField(help_text="Enter your country.", label="Country", required=True)
    province = forms.CharField(help_text="Enter your province.", label="Province", required=True)
    city = forms.CharField(help_text="Enter your city.", label="City", required=True)
    postal_code = forms.CharField(help_text="Enter your postal code.", label="Postal Code", required=True)
    street = forms.CharField(help_text="Enter your street.", label="Street", required=True)
    house_number = forms.CharField(help_text="Enter your house number.", label="House Number", required=True)
    apartment_number = forms.CharField(help_text="Enter your apartment number.", label="Apartment Number",
                                       required=False)

    class Meta:
        model = ProfileContactInformation
        fields = "__all__"


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True

        self.fields["basic_information"].help_text = "Select the basic information for this user."
        self.fields["basic_information"].label = "Basic Information"
        self.fields["basic_information"].required = True

        self.fields["contact_information"].help_text = "Select the contact information for this user."
        self.fields["contact_information"].label = "Contact Information"
        self.fields["contact_information"].required = True

        self.fields["contract"].help_text = "Select the contract for this user"
        self.fields["contract"].label = "Contract"
        self.fields["contract"].required = True


class AdminProfileImageForm(forms.ModelForm):
    image = forms.ImageField(
        help_text="Upload a profile image.",
        label="Profile Image",
        required=False,
    )
    size = forms.IntegerField(
        required=False
    )
    width = forms.IntegerField(
        required=False
    )
    height = forms.IntegerField(
        required=False
    )
    format = forms.CharField(
        required=False,
    )
    alt = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )

    class Meta:
        model = ProfileImage
        fields = [
            "created_at",
            "image",
            "size",
            "width",
            "height",
            "format",
            "alt",
        ]


class PasswordResetForm(forms.Form):
    mobile = forms.CharField(
        required=False,
    )
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        }
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput,
        required=False,
    )
    repassword = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile").strip()

        if "email" and "mobile" in self.data:
            if not mobile:
                raise ValidationError(
                    message="Phone Number is required.",
                )

            if not re.compile(r"^\d{8,15}$").match(mobile):
                raise ValidationError(
                    message="Invalid phone number format. Please enter a valid number with the country code (e.g., 11234567890 for the USA).",
                )

        return mobile

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()

        if not email:
            raise ValidationError(
                message="Email is required.",
            )

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        if not User.objects.filter(email=email).exists():
            raise ValidationError(
                message=f"A user with the email address '{email}' does not exist.",
            )

        return email


class OneTimePasswordForm(forms.Form):
    email = forms.CharField(
        required=False,
    )
    password = forms.CharField(
        error_messages={
            "required": "One Time Password is required.",
        },
        required=True,
    )

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(email=email)
            otp = OneTimePassword.objects.get(user=user)

        except User.DoesNotExist:
            raise ValidationError(
                message=f"A user with the email address '{email}' does not exist.",
            )

        except OneTimePassword.DoesNotExist:
            raise ValidationError(
                message=f"The One Time Password for the user '{email}' does not exist."
            )

        otp = OneTimePassword.objects.get(user=user).password

        if otp != password:
            raise ValidationError(
                message=f"Incorrect One Time Password for the user '{email}'. Please try again.",
            )

        return password


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        required=True,
        widget=forms.PasswordInput
    )
    repassword = forms.CharField(
        error_messages={
            "required": "Confirm Password is required.",
        },
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "password",
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError(
                message="The password should consist of at least 8 characters.",
            )

        if len(password) > 255:
            raise ValidationError(
                message="The password cannot be longer than 255 characters.",
            )

        if not re.match(pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", string=password):
            raise ValidationError(
                message="The password should contain at least one uppercase letter, one lowercase letter, one number, "
                        "and one special character.",
            )

        return password

    def clean_repassword(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")

        if password is not None:
            if not repassword:
                raise ValidationError(
                    message="Confirm Password is required.",
                )

            if repassword != password:
                raise ValidationError(
                    message="Confirm Password does not match.",
                )

        return repassword


class UpdateProfileImageForm(forms.Form):
    profile_image = forms.ImageField(
        required=False,
    )

    def clean_profileimage(self):
        profile_image = self.cleaned_data.get("profileimage")
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]

        if profile_image:
            if profile_image.name.split(".")[-1] not in allowed_extensions:
                raise ValidationError(
                    message="Invalid file format, allowed formats are 'jpg', 'jpeg', 'png', 'webp'.",
                )

            if profile_image.size > 1000000:
                raise ValidationError(
                    message="File size too large, the maximum allowed size is 1MB.",
                )

            try:
                img = Image.open(fp=profile_image)
                img.verify()

            except(IOError, SyntaxError):
                raise ValidationError(
                    message="The file is not a valid image.",
                )

        return profile_image
