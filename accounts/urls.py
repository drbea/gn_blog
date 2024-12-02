from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_page, name="login"),

    path("register/", views.register_page, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    path("user_profile/<str:user_id>/", views.user_profile, name="user_profile"),
]
