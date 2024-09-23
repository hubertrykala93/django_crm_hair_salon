from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="home")
def dashboard(request):
    return render(
        request=request,
        template_name="core/dashboard.html",
        context={
            "title": "Dashboard",
        },
    )
