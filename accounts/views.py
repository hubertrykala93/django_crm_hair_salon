from django.shortcuts import render, redirect, reverse
from .forms import PasswordResetForm, OneTimePasswordForm, ChangePasswordForm
from django.contrib import messages
from .models import User, OneTimePassword
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


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
            user = User.objects.get(email=form.cleaned_data.get("email"))

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
                        message=f"We have sent the password to the provided email address '{form.cleaned_data.get('email')}'. Please check your inbox.",
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
            if request.POST["password"] != request.POST["repassword"]:
                form.add_error(
                    field="repassword",
                    error="Confirm Password does not match.",
                )

            else:
                try:
                    user = User.objects.get(email=request.GET["email"])
                    otp = OneTimePassword.objects.get(user=user)

                    user.set_password(raw_password=request.POST["password"])
                    user.is_active = True
                    user.save()

                    otp.delete()

                    messages.success(
                        request=request,
                        message=f"The password for the account '{user.email}' has been successfully changed. "
                                f"You can now log in.",
                    )

                    return redirect(to="index")

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


@login_required(login_url="index")
def log_out(request):
    logout(request=request)

    return redirect(to="index")
