from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route="", view=accounts_views.index, name="home"),
    path(route="register", view=accounts_views.register, name="register"),
    path(route="activate/<uidb64>/<token>", view=accounts_views.activate, name="activate"),
    path(route="choose-method", view=accounts_views.password_reset_method, name="choose-method"),
    path(route="forgot-password", view=accounts_views.forgot_password, name="forgot-password"),
    path(route="confirm-password", view=accounts_views.confirm_one_time_password, name="confirm-password"),
    path(route="change-password", view=accounts_views.change_password, name="change-password"),
    path(route="profile", view=accounts_views.profile, name="profile"),
    path(route="update-profile-form", view=accounts_views.update_profile_form, name="update-profile-form"),
    path(route="logout", view=accounts_views.log_out, name="logout"),
    path(route="contact-us", view=accounts_views.contact_us, name="contact-us"),
]
