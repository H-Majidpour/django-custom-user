from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("resend_confirmation/", views.resend_confirmation_email, name="resend_confirmation"),
]