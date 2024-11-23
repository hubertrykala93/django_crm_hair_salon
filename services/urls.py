from django.urls import path
from . import views as services_views

urlpatterns = [
    path(route="services", view=services_views.services, name="services"),
]
