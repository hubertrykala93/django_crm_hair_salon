from django.shortcuts import render
from .models import Service


def services(request):
    return render(
        request=request,
        template_name="services/services.html",
        context={
            "title": "Services",
            "services": Service.objects.all(),
        }
    )
