from django import forms
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation, \
    ProfileEmploymentInformation, JobPosition, EmploymentStatus, Contract
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
    is_verified = forms.BooleanField(
        help_text="Check if the user should be verified.",
        required=False
    )
    is_active = forms.BooleanField(
        help_text="Check if the user should be active.",
        required=True
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
            "user_permissions",
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
    firstname = forms.CharField(help_text="Enter first name.", label="First Name", required=False)
    lastname = forms.CharField(help_text="Enter last name.", label="Last Name", required=False)
    date_of_birth = forms.DateField(help_text="Enter date of birth.", label="Date of Birth", required=False)
    biography = forms.CharField(help_text="Enter biography.", label="Biography", required=False, widget=forms.Textarea)

    class Meta:
        model = ProfileBasicInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileBasicInformationForm, self).__init__(*args, **kwargs)

        self.fields["profile_image"].help_text = "Select the profile image."
        self.fields["profile_image"].label = "Profile Image"
        self.fields["profile_image"].required = False


class AdminProfileContactInformationForm(forms.ModelForm):
    phone_number = forms.CharField(help_text="Enter phone number.", label="Phone Number", required=False)
    country = forms.CharField(help_text="Enter country.", label="Country", required=False)
    province = forms.CharField(help_text="Enter province.", label="Province", required=False)
    city = forms.CharField(help_text="Enter city.", label="City", required=False)
    postal_code = forms.CharField(help_text="Enter postal code.", label="Postal Code", required=False)
    street = forms.CharField(help_text="Enter street.", label="Street", required=False)
    house_number = forms.CharField(help_text="Enter house number.", label="House Number", required=False)
    apartment_number = forms.CharField(help_text="Enter apartment number.", label="Apartment Number", required=False)

    class Meta:
        model = ProfileContactInformation
        fields = "__all__"


class AdminJobPositionForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter job position name.", label_suffix="Job Position", required=True)

    class Meta:
        model = JobPosition
        fields = "__all__"


class AdminEmploymentStatusForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter employment status name.", label_suffix="Employment Status", required=True)

    class Meta:
        model = EmploymentStatus
        fields = "__all__"


class AdminContractForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter contract name.", label="Contract", required=True)
    start_date = forms.DateField(help_text="Enter the start of the contract.", label="Start Date", required=True)
    end_date = forms.DateField(help_text="Enter the end of the contract.", label="End Date", required=False)
    salary = forms.DecimalField(help_text="Enter the salary.", label="Contract Salary", required=True)
    work_hours_per_week = forms.IntegerField(help_text="Enter the number of working hours per week.",
                                             label="Working Hours", required=False)

    class Meta:
        model = Contract
        exclude = ["duration"]


class AdminProfileEmploymentInformationForm(forms.ModelForm):
    class Meta:
        model = ProfileEmploymentInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileEmploymentInformationForm, self).__init__(*args, **kwargs)

        self.fields["job_position"].help_text = "Select job position."
        self.fields["employment_status"].help_text = "Select employment status."
        self.fields["contract"].help_text = "Select contract."

        self.fields["job_position"].label = "Job Position"
        self.fields["employment_status"].label = "Employment Status"
        self.fields["contract"].label = "Contract"

        self.fields["job_position"].required = True
        self.fields["employment_status"].required = True
        self.fields["contract"].required = True


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True

        self.fields["basicinformation"].help_text = "Select the basic information for this user."
        self.fields["basicinformation"].label = "Basic Information"
        self.fields["basicinformation"].required = True

        self.fields["contactinformation"].help_text = "Select the contact information for this user."
        self.fields["contactinformation"].label = "Contact Information"
        self.fields["contactinformation"].required = True

        self.fields["employmentinformation"].help_text = "Select the employment information for this user."
        self.fields["employmentinformation"].label = "Employment Information"
        self.fields["employmentinformation"].required = True


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
        required=True,
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


class RegisterForm(forms.ModelForm):
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

    )
    repassword = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "password", "repassword"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                message=f"The user with the e-mail address '{email}' already exists.",
            )

        return email

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


class LoginForm(forms.Form):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        },
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput,
    )
    remember = forms.BooleanField(
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

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

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(raw_password=password):
                raise ValidationError(
                    message=f"Incorrect password for the account '{email}'.",
                )

        return password


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
        mobile = self.cleaned_data.get("mobile")

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
    email = self.cleaned_data.get("email")

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

    if User.objects.filter(email=email).exists() and not User.objects.get(email=email).is_verified:
        raise ValidationError(
            message=f"Your account has not been verified yet. To reset the password, you must first verify your account.",
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
    profileimage = forms.ImageField(
        required=False,
    )

    def clean_profileimage(self):
        profileimage = self.cleaned_data.get("profileimage")
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]

        if profileimage:
            if profileimage.name.split(".")[-1] not in allowed_extensions:
                raise ValidationError(
                    message="Invalid file format, allowed formats are 'jpg', 'jpeg', 'png', 'webp'.",
                )

            if profileimage.size > 1000000:
                raise ValidationError(
                    message="File size too large, the maximum allowed size is 1MB.",
                )

            try:
                img = Image.open(fp=profileimage)
                img.verify()

            except(IOError, SyntaxError):
                raise ValidationError(
                    message="The file is not a valid image.",
                )

        return profileimage


class UpdateUserForm(forms.Form):
    email = forms.CharField(
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
    repassword = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email != "":
            if len(email) > 255:
                raise ValidationError(
                    message="The e-mail address cannot be longer than 255 characters.",
                )

            if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                            string=email):
                raise ValidationError(
                    message="The e-mail address format is invalid.",
                )

            if self.instance.email != email:
                if User.objects.filter(email=email).exists():
                    raise ValidationError(
                        message=f"The user with the e-mail address '{email}' already exists.",
                    )

            if self.instance.email == email:
                raise ValidationError(
                    message="The email address cannot be changed to the same one. Please enter a new email address.",
                )

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password:
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

            if self.instance.check_password(raw_password=password):
                raise ValidationError(
                    message="The password cannot be changed to the same one. Please enter a new email address.",
                )

        return password

    def clean_repassword(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")

        if password:
            if not repassword:
                raise ValidationError(
                    message="Confirm Password is required.",
                )

            if repassword != password:
                raise ValidationError(
                    message="Confirm Password does not match.",
                )

        else:
            if repassword:
                raise ValidationError(
                    message="You must also provide the password.",
                )

        return repassword


class UpdateProfileForm(forms.Form):
    firstname = forms.CharField(
        error_messages={
            "required": "Firstname is required.",
        },
    )
    lastname = forms.CharField(
        error_messages={
            "required": "Lastname is required.",
        },
    )
    biography = forms.CharField(
        required=False,
    )
    dateofbirth = forms.CharField(
        error_messages={
            "required": "Date of Birth is required.",
        }
    )
    phonenumber = forms.CharField(
        error_messages={
            "required": "Phone Number is required.",
        }
    )
    country = forms.CharField(
        error_messages={
            "required": "Country is required.",
        }
    )
    province = forms.CharField(
        error_messages={
            "required": "Province is required.",
        }
    )
    city = forms.CharField(
        error_messages={
            "required": "City is required.",
        }
    )
    postalcode = forms.CharField(
        error_messages={
            "required": "Postal Code is required.",
        }
    )
    street = forms.CharField(
        error_messages={
            "required": "Street is required.",
        }
    )
    housenumber = forms.CharField(
        error_messages={
            "required": "House Number is required.",
        }
    )
    apartmentnumber = forms.CharField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname")

        if len(firstname) < 2:
            raise ValidationError(
                message="The firstname should contain at least 2 characters.",
            )

        if len(firstname) > 50:
            raise ValidationError(
                message="The firstname should contain a maximum of 50 characters.",
            )

        if not firstname.isalpha():
            raise ValidationError(
                message="The firstname should consist of letters only.",
            )

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname")

        if len(lastname) < 2:
            raise ValidationError(
                message="The lastname should contain at least 2 characters."
            )

        if len(lastname) > 100:
            raise ValidationError(
                message="The lastname should contain a maximum of 100 characters.",
            )

        if not lastname.isalpha():
            raise ValidationError(
                message="The lastname should consist of letters only.",
            )

        return lastname

    def clean_dateofbirth(self):
        dateofbirth = self.cleaned_data.get("dateofbirth")

        try:
            date_object = datetime.strptime(dateofbirth, "%Y-%m-%d").date()

        except ValueError:
            raise ValidationError(
                message="Date must be in the format YYYY-MM-DD.",
            )

        if date_object >= date.today():
            raise ValidationError(
                message="The date of birth cannot be greater than or equal to the current date.",
            )

        if not re.match(pattern="^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", string=dateofbirth):
            raise ValidationError(
                message="Date must be in the format YYYY-MM-DD.",
            )

        return dateofbirth

    def clean_biography(self):
        biography = self.cleaned_data.get("biography")

        if biography:
            if len(biography) < 10:
                raise ValidationError(
                    message="The biography should contain at least 10 characters.",
                )

            if len(biography) > 200:
                raise ValidationError(
                    message="The biography should contain a maximum of 200 characters.",
                )

        return biography

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get("phonenumber")

        if not re.match(pattern="^\+?\d{0,3}?[-. (]?\d{3}[-. )]?\d{3}[-. ]?\d{3}$", string=phonenumber):
            raise ValidationError(
                message="Invalid phone number format.",
            )

        return phonenumber

    def clean_country(self):
        country = self.cleaned_data.get("country")

        if len(country) < 4:
            raise ValidationError(
                message="The country should contain at least 4 characters.",
            )

        if len(country) > 56:
            raise ValidationError(
                message="The country should contain a maximum of 56 characters.",
            )

    def clean_province(self):
        province = self.cleaned_data.get("province")

        if len(province) < 3:
            raise ValidationError(
                message="The province should contain at least 3 characters.",
            )

        if len(province) > 23:
            raise ValidationError(
                message="The province should contain a maximum of 23 characters.",
            )

        return province

    def clean_city(self):
        city = self.cleaned_data.get("city")

        if len(city) > 85:
            raise ValidationError(
                message="The city should contain a maximum of 85 characters.",
            )

        return city

    def clean_postalcode(self):
        postalcode = self.cleaned_data.get("postalcode")

        if len(postalcode) < 3:
            raise ValidationError(
                message="The postal code should contain at least 3 characters.",
            )

        if len(postalcode) > 10:
            raise ValidationError(
                message="The postal code should contain a maximum of 10 characters.",
            )

        return postalcode

    def clean_street(self):
        street = self.cleaned_data.get("street")

        if len(street) > 58:
            raise ValidationError(
                message="The city should contain a maximum of 58 characters.",
            )

        return street

    def clean_housenumber(self):
        housenumber = self.cleaned_data.get("housenumber")

        if len(housenumber) > 10:
            raise ValidationError(
                message="The house number should contain a maximum of 10 characters.",
            )

        return housenumber

    def clean_apartmentnumber(self):
        apartmentnumber = self.cleaned_data.get("apartmentnumber")

        if len(apartmentnumber) > 10:
            raise ValidationError(
                message="The apartment number should contain a maximum of 10 characters.",
            )

        return apartmentnumber


class ContactUsForm(forms.Form):
    firstname = forms.CharField(
        error_messages={
            "required": "Firstname is required.",
        }
    )
    lastname = forms.CharField(
        error_messages={
            "required": "Lastname is required.",
        }
    )
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        }
    )
    subject = forms.CharField(
        error_messages={
            "required": "Subject is required.",
        }
    )
    message = forms.CharField(
        error_messages={
            "required": "Message is required.",
        }
    )

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname")

        if len(firstname) < 2:
            raise ValidationError(
                message="The firstname should contain at least 2 characters.",
            )

        if len(firstname) > 50:
            raise ValidationError(
                message="The firstname should contain a maximum of 50 characters.",
            )

        if not firstname.isalpha():
            raise ValidationError(
                message="The firstname should consist of letters only.",
            )

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname")

        if len(lastname) < 2:
            raise ValidationError(
                message="The lastname should contain at least 2 characters."
            )

        if len(lastname) > 100:
            raise ValidationError(
                message="The lastname should contain a maximum of 100 characters.",
            )

        if not lastname.isalpha():
            raise ValidationError(
                message="The lastname should consist of letters only.",
            )

        return lastname

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")

        if len(subject) < 10:
            raise ValidationError(
                message="The subject should contain at least 10 characters.",
            )

        if len(subject) > 50:
            raise ValidationError(
                message="The lastname should contain a maximum of 50 characters.",
            )

        return subject

    def clean_message(self):
        message = self.cleaned_data.get("message")

        if len(message) < 20:
            raise ValidationError(
                message="The message should contain at least 20 characters.",
            )

        if len(message) > 500:
            raise ValidationError(
                message="The message should contain a maximum of 500 characters.",
            )

        return message
