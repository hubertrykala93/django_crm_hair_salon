from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm, PasswordResetForm, OneTimePasswordForm, ChangePasswordForm, UpdateUserForm, \
    UpdateProfileImageForm, UpdateProfileForm
from django.contrib import messages
from .models import User, OneTimePassword
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def index(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=User.objects.get(email=request.POST["email"]).username,
                password=request.POST["password"],
            )

            if user.is_verified:
                if user is not None:
                    if "remember" in request.POST:
                        request.session["user_id"] = user.id
                        request.session.set_expiry(value=1000000)
                        request.session.modified = True

                    login(
                        request=request,
                        user=user,
                    )

                    messages.success(
                        request=request,
                        message="You have been logged in successfully.",
                    )

                    return redirect(to="dashboard")

            else:
                messages.info(
                    request=request,
                    message="Your account has not been activated yet. Please activate your account to log in.",
                )

    else:
        form = LoginForm()

    return render(
        request=request,
        template_name="accounts/login.html",
        context={
            "title": "Login",
            "form": form,
        }
    )


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = User(
                email=request.POST["email"]

            )
            password = make_password(
                password=request.POST["password"]
            )
            user.password = password
            user.save()

            try:
                html_message = render_to_string(
                    template_name="accounts/account-activation-email.html",
                    context={
                        "user": user,
                        "domain": get_current_site(request=request),
                        "uid": urlsafe_base64_encode(s=force_bytes(s=user.pk)),
                        "token": token_generator.make_token(user=user)
                    },
                    request=request,
                )
                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject="Account Activation Request",
                    body=plain_message,
                    to=[user.email],
                )
                message.attach_alternative(content=html_message, mimetype="text/html")
                message.send()

                user.save()

                messages.success(
                    request=request,
                    message="Your account has been successfully created. Please check your email to activate it.",
                )

                return redirect(to="register")

            except Exception as e:
                messages.error(
                    request=request,
                    message="Registration failed. Please try again.",
                )

                return redirect(to="register")

        else:
            if len(request.POST["password"]) != 0 and len(request.POST["repassword"]) == 0:
                messages.error(
                    request=request,
                    message="To register an account, you also need to provide the Confirm Password.",
                )

    else:
        form = RegisterForm()

    return render(
        request=request,
        template_name="accounts/register.html",
        context={
            "title": "Register",
            "form": form,
        },
    )


def activate(request, uidb64, token):
    try:
        uid = force_str(s=urlsafe_base64_decode(s=uidb64))
        user = User.objects.get(pk=int(uid))

    except User.DoesNotExist:
        messages.info(
            request=request,
            message="Your account does not exist, please register.",
        )

        return redirect(to="register")

    if user:
        if not user.is_verified:

            if token_generator.check_token(user=user, token=token):
                user.is_verified = True
                user.save()

                messages.success(
                    request=request,
                    message="Your account has been activated, you can now log in."
                )

            else:
                user.delete()

                messages.info(
                    request=request,
                    message="Your activation link has expired. Please create your account again.",
                )

                return redirect(to="register")

        else:
            messages.info(
                request=request,
                message="Your account has already been activated, you can log in.",
            )

    return redirect(to="home")


def password_reset_method(request):
    if request.method == "POST":
        if "method" in request.POST:
            if request.POST["method"] == "email":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

            elif request.POST["method"] == "sms":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

            elif request.POST["method"] == "voice":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

    return render(
        request=request,
        template_name="accounts/password-reset-method.html",
        context={
            "title": "Choose Method",
        }
    )


def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)

        if form.is_valid():
            user = User.objects.get(email=request.POST["email"])

            if not OneTimePassword.objects.filter(user=user).exists():
                otp = OneTimePassword(user=user)
                otp.save()

            otp = OneTimePassword.objects.get(user=user)

            if request.GET["method"] == "email":
                try:
                    html_message = render_to_string(
                        template_name="accounts/password-reset-email.html",
                        context={
                            "user": user,
                            "otp": otp.password,
                        },
                        request=request,
                    )
                    plain_message = strip_tags(html_message)

                    message = EmailMultiAlternatives(
                        subject="Password Reset Request",
                        body=plain_message,
                        to=[user.email],
                    )
                    message.attach_alternative(content=html_message, mimetype="text/html")
                    message.send()

                    messages.success(
                        request=request,
                        message=f"We have sent the password to the provided email address '{request.POST['email']}'. Please check your inbox.",
                    )

                    return redirect(f"{reverse('confirm-password')}?method={request.GET['method']}&email={user.email}")


                except Exception as e:
                    messages.error(
                        request=request,
                        message="Failed to send the email, please try again.",
                    )

                    return redirect(to=reverse(viewname="forgot-password") + f"?method={request.GET['method']}")

            else:
                if request.GET["method"] == "sms":
                    pass

                else:
                    pass

                return redirect(to=reverse(
                    viewname="confirm-password") + f"?method={request.GET['method']}&mobile={request.POST['mobile']}")

    else:
        form = PasswordResetForm()

    return render(
        request=request,
        template_name="accounts/forgot-password.html",
        context={
            "title": "Forgot Password",
            "form": form,
        }
    )


def confirm_one_time_password(request):
    if request.method == "POST":
        form = OneTimePasswordForm(data=request.POST)

        if form.is_valid():
            user = User.objects.get(email=request.GET["email"])

            return redirect(f"{reverse('change-password')}?email={user.email}")

    else:
        form = OneTimePasswordForm()

    return render(
        request=request,
        template_name="accounts/confirm-password.html",
        context={
            "title": "Confirm Password",
            "form": form,
        }
    )


def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(
            data=request.POST,
        )

        if form.is_valid():
            try:
                user = User.objects.get(email=request.GET["email"])
                otp = OneTimePassword.objects.get(user=user)

                user.set_password(raw_password=request.POST["password"])
                user.save()

                otp.delete()

                messages.success(
                    request=request,
                    message=f"The password for the account '{user.email}' has been successfully changed. "
                            f"You can now log in.",
                )

                return redirect(to="home")

            except User.DoesNotExist:
                messages.info(
                    request=request,
                    message=f"A user with the email address '{request.GET['email']}' does not exist."
                )

                return redirect(to="register")

            except OneTimePassword.DoesNotExist:
                messages.info(
                    request=request,
                    message=f"The One Time Password for the user '{request.GET['email']}' does not exist.",
                )

                return redirect(to="forgot-password")

    else:
        form = ChangePasswordForm()

    return render(
        request=request,
        template_name="accounts/change-password.html",
        context={
            "title": "Change Password",
            "form": form,
        }
    )


def profile(request):
    if request.method == "POST":
        profileimage_update_form = UpdateProfileImageForm(files=request.FILES, prefix="profileimage")
        update_user_form = UpdateUserForm(data=request.POST, instance=request.user, prefix="user")
        update_profile_form = UpdateProfileForm(data=request.POST, prefix="profile")

        if "update-profile-image" in request.POST:
            if profileimage_update_form.is_valid():
                profile_image_uploaded = request.FILES.get("profileimage", None)

                if profile_image_uploaded is not None:
                    profile_image = request.user.profile.basicinformation.profileimage
                    profile_image.image = request.FILES["profileimage"]
                    profile_image.save()

                    messages.success(
                        request=request,
                        message="Profile picture has been successfully changed.",
                    )

            else:
                print(profileimage_update_form.errors)

        if "update-user" in request.POST:
            if update_user_form.is_valid():
                user = request.user
                password = request.POST.get("password", None)

                if password:
                    if request.user.email == request.POST["email"]:
                        user.set_password(raw_password=request.POST["password"])
                        user.save()

                    else:
                        user.email = request.POST["email"]
                        user.set_password(raw_password=request.POST["password"])
                        user.save()

                else:
                    user.email = request.POST["email"]
                    user.save()

                update_session_auth_hash(request=request, user=user)

                messages.success(
                    request=request,
                    message="Account details have been successfully changed.",
                )

            else:
                print(update_user_form.errors)

        if "update-profile" in request.POST:
            if update_profile_form.is_valid():
                profile = request.user.profile

                original_firstname = profile.basicinformation.firstname
                original_lastname = profile.basicinformation.lastname
                original_dateofbirth = profile.basicinformation.dateofbirth
                original_biography = profile.basicinformation.biography

                original_phonenumber = profile.contactinformation.phonenumber
                original_country = profile.contactinformation.country
                original_province = profile.contactinformation.province
                original_city = profile.contactinformation.city
                original_street = profile.contactinformation.street
                original_housenumber = profile.contactinformation.housenumber
                original_apartmentnumber = profile.contactinformation.apartmentnumber

                changed_fields = (
                        original_firstname != request.POST["firstname"] or
                        original_lastname != request.POST["lastname"] or
                        original_dateofbirth.strftime("%Y-%m-%d") != request.POST["dateofbirth"] or
                        original_biography != request.POST["biography"] or
                        original_phonenumber != request.POST["phonenumber"] or
                        original_country != request.POST["country"] or
                        original_province != request.POST["province"] or
                        original_city != request.POST["city"] or
                        original_street != request.POST["street"] or
                        original_housenumber != request.POST["housenumber"] or
                        original_apartmentnumber != request.POST["apartmentnumber"]
                )

                if changed_fields:
                    messages.success(
                        request=request,
                        message="Profile details have been successfully changed.",
                    )

                else:
                    messages.info(
                        request=request,
                        message="No changes have been made.",
                    )

            else:
                print(update_profile_form.errors)

    else:
        print(f"Request POST -> {request.POST}")
        profileimage_update_form = UpdateProfileImageForm()
        update_user_form = UpdateUserForm(instance=request.user)
        update_profile_form = UpdateProfileForm()

    print(f"Update User Form Data -> {update_user_form.data}")

    return render(
        request=request,
        template_name="accounts/profile.html",
        context={
            "title": "Profile",
            "profileimage_update_form": profileimage_update_form,
            "update_user_form": update_user_form,
            "update_profile_form": update_profile_form,
        }
    )


def update_profile_form(request):
    form = UpdateProfileForm(data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            messages.success(
                request=request,
                message="Profile details have been successfully changed.",
            )

            return redirect(to="profile")

    return render(
        request=request,
        template_name="accounts/profile.html",
        context={
            "update_profile_form": form,
        }
    )


def log_out(request):
    logout(request=request)

    return redirect(to="home")
