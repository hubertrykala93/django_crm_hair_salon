from django.urls import path
from . import views as company_views

urlpatterns = [
    path(route="", view=company_views.index, name="home"),
    path(route="register", view=company_views.register, name="register"),
]
