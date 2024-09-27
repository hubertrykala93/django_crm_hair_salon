from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, PasswordResetForm, OneTimePasswordForm, ChangePasswordForm, \
    UpdateContactInformationForm, UpdatePasswordForm, UpdateBasicInformationForm, \
    UpdatePaymentInformationForm
from django.contrib import messages
from .models import User, OneTimePassword
from contracts.models import PaymentFrequency
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator
from datetime import date, datetime


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


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
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


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
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


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
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


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
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


@login_required(login_url="home")
def settings(request):
    update_password_form = UpdatePasswordForm()
    update_basic_information_form = UpdateBasicInformationForm(initial={
        "date_of_birth": request.user.profile.basic_information.date_of_birth.strftime(
            "%Y-%m-%d") if request.user.profile.basic_information.date_of_birth else "",
    })
    update_contact_information_form = UpdateContactInformationForm()
    update_payment_information_form = UpdatePaymentInformationForm()

    if request.method == "POST":
        if "change-password" in request.POST:
            update_password_form = UpdatePasswordForm(data=request.POST, instance=request.user)

            if update_password_form.is_valid():
                password = request.POST["password"]

                if password:
                    user = request.user

                    if user.check_password(raw_password=password):
                        messages.info(
                            request=request,
                            message="You cannot change to the previous password; please create a new one.",
                        )
                    else:
                        user.set_password(raw_password=password)
                        user.save()

                        update_session_auth_hash(
                            request=request,
                            user=user
                        )

                        messages.success(
                            request=request,
                            message="The password has been successfully changed.",
                        )

                else:
                    messages.info(
                        request=request,
                        message="No changes have been made.",
                    )

        if "basic-information" in request.POST:
            update_basic_information_form = UpdateBasicInformationForm(data=request.POST)

            if update_basic_information_form.is_valid():
                changes = {}

                basic_information = request.user.profile.basic_information

                if basic_information.firstname != request.POST["firstname"]:
                    changes.update(
                        {
                            "firstname": request.POST["firstname"],
                        },
                    )

                if basic_information.lastname != request.POST["lastname"]:
                    changes.update(
                        {
                            "lastname": request.POST["lastname"],
                        },
                    )

                if basic_information.date_of_birth != datetime.strptime(request.POST["date_of_birth"],
                                                                        "%Y-%m-%d").date():
                    changes.update(
                        {
                            "date_of_birth": request.POST["date_of_birth"],
                        },
                    )

                if request.POST["biography"]:
                    if basic_information.biography != request.POST["biography"]:
                        changes.update(
                            {
                                "biography": request.POST["biography"],
                            },
                        )

                if changes:
                    for name, value in changes.items():
                        setattr(basic_information, name, value.strip() if isinstance(value, str) else value)

                    basic_information.save()

                    messages.success(
                        request=request,
                        message="Basic Information has been successfully updated."
                    )

                else:
                    messages.info(
                        request=request,
                        message="No changes have been made."
                    )

        if "contact-information" in request.POST:
            update_contact_information_form = UpdateContactInformationForm(data=request.POST)

            if update_contact_information_form.is_valid():
                changes = {}
                contact_information = request.user.profile.contact_information

                if contact_information.phone_number != request.POST["phone_number"]:
                    changes.update(
                        {
                            "phone_number": request.POST["phone_number"],
                        },
                    )

                if contact_information.country != request.POST["country"]:
                    changes.update(
                        {
                            "country": request.POST["country"],
                        },
                    )

                if contact_information.province != request.POST["province"]:
                    changes.update(
                        {
                            "province": request.POST["province"],
                        },
                    )

                if contact_information.city != request.POST["city"]:
                    changes.update(
                        {
                            "city": request.POST["city"],
                        },
                    )

                if contact_information.postal_code != request.POST["postal_code"]:
                    changes.update(
                        {
                            "postal_code": request.POST["postal_code"],
                        },
                    )

                if contact_information.street != request.POST["street"]:
                    changes.update(
                        {
                            "street": request.POST["street"],
                        },
                    )

                if contact_information.house_number != request.POST["house_number"]:
                    changes.update(
                        {
                            "house_number": request.POST["house_number"],
                        },
                    )

                if request.POST["apartment_number"]:
                    if contact_information.apartment_number != request.POST["apartment_number"]:
                        changes.update(
                            {
                                "apartment_number": request.POST["apartment_number"],
                            },
                        )

                if changes:
                    for name, value in changes.items():
                        setattr(contact_information, name, value.strip() if isinstance(value, str) else value)

                    contact_information.save()

                    messages.success(
                        request=request,
                        message="Contact Information has been successfully updated.",
                    )

                else:
                    messages.info(
                        request=request,
                        message="No changes have been made.",
                    )

        if "payment-information" in request.POST:
            update_payment_information_form = UpdatePaymentInformationForm(
                data=request.POST,
                instance=request.user.profile.payment_information
            )

            if update_payment_information_form.is_valid():
                changes = {}
                payment_information = request.user.profile.payment_information

                if payment_information.iban != request.POST["iban"]:
                    changes.update(
                        {
                            "iban": request.POST["iban"],
                        },
                    )

                if payment_information.account_number != request.POST["account_number"]:
                    changes.update(
                        {
                            "account_number": request.POST["account_number"],
                        },
                    )

                if changes:
                    for name, value in changes.items():
                        setattr(payment_information, name, value.strip() if isinstance(value, str) else value)

                    payment_information.save()

                    messages.success(
                        request=request,
                        message="Payment Information has been successfully updated.",
                    )

                else:
                    messages.info(
                        request=request,
                        message="No changes have been made.",
                    )

    time_remaining = None

    if request.user.profile.employment_information.contract.end_date:
        time_remaining = request.user.profile.employment_information.contract.end_date - date.today()

    return render(
        request=request,
        template_name="accounts/settings.html",
        context={
            "title": "Profile",
            "benefits": request.user.profile.employment_information.contract.benefits,
            "time_remaining": time_remaining,
            "update_password_form": update_password_form,
            "update_basic_information_form": update_basic_information_form,
            "update_contact_information_form": update_contact_information_form,
            "update_payment_information_form": update_payment_information_form,
        }
    )


@login_required(login_url="home")
def log_out(request):
    logout(request=request)

    return redirect(to="home")
