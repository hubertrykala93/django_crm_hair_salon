from django.shortcuts import render


def services(request):
    return render(
        request=request,
        template_name="services/services.html",
        context={
            "title": "Services",
        }
    )
