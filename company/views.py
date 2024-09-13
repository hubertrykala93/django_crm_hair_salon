from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages


def index(request):
    return render(
        request=request,
        template_name="company/login.html",
        context={
            "title": "Login",
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            print("Form is Valid.")
            messages.success(
                request=request,
                message="Your account has been successfully created. Please check your email to activate it.",
            )
            return redirect(to="home")

        else:
            print("Form is not Valid.")

    else:
        print("Request method is not POST.")
        form = RegisterForm()

    return render(
        request=request,
        template_name="company/register.html",
        context={
            "title": "Register",
            "form": form,
        }
    )
