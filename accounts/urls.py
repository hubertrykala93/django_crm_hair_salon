from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route="", view=accounts_views.index, name="home"),
    path(route="register", view=accounts_views.register, name="register"),
    path(route="activate/<uidb64>/<token>", view=accounts_views.activate, name="activate"),
    path(route="forgot-password", view=accounts_views.forgot_password, name="forgot-password"),
    path(route="logout", view=accounts_views.log_out, name="logout"),
]
