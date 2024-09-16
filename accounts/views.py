from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, PasswordResetForm
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator
import os


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def index(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=User.objects.get(email=request.POST["email"]).username,
                password=request.POST["password"],
            )

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
        form = RegisterForm()

    return render(
        request=request,
        template_name="accounts/register.html",
        context={
            "title": "Register",
            "form": form,
        }
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


def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)

        if form.is_valid():
            print("Form is valid.")


        else:
            print(form.errors)
            print("Form is not valid.")

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
    return render(
        request=request,
        template_name="accounts/confirm-one-time-password.html",
        context={
            "Confirm Password",
        }
    )


def change_password(request):
    return render(
        request=request,
        template_name="accounts/change-password.html",
        context={
            "title": "Change Password",
        }
    )


def log_out(request):
    logout(request=request)

    return redirect(to="home")
