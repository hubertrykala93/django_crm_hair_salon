from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def index(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            print("Form is Valid.")
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

            messages.success(
                request=request,
                message="Your account has been successfully created. Please check your email to activate it.",
            )

            return redirect(to="home")

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


def log_out(request):
    logout(request=request)

    return redirect(to="home")
