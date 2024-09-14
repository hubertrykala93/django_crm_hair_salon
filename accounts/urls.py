from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route="", view=accounts_views.index, name="home"),
    path(route="register", view=accounts_views.register, name="register"),
    path(route="logout", view=accounts_views.log_out, name="logout"),
]
