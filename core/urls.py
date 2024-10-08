from django.urls import path
from . import views as core_views

urlpatterns = [
    path(route="", view=core_views.index, name="index"),
    path(route="contact-us", view=core_views.contact_us, name="contact-us"),
    path(route="dashboard", view=core_views.dashboard, name="dashboard"),
    # path(route="register-employee", view=core_views.register_employee, name="register-employee"),
]
