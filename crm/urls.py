"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import development as development_settings
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="", view=include(arg="accounts.urls")),
    path(route="", view=include(arg="core.urls")),
    path(route="", view=include(arg="invoices.urls")),
    path(route="", view=include(arg="dashboard.urls")),
    path(route="", view=include(arg="employees.urls")),
    path(route="", view=include(arg="services.urls")),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(prefix=development_settings.MEDIA_URL, document_root=development_settings.MEDIA_ROOT)
