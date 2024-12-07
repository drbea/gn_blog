from django.urls import path

from . import views 

app_name = "accounts"

urlpatterns = [
    path("", views.login_page, name="login"),

    path("deconnexion/", views.logout_suer, name="deconnexion"),
    path("register/", views.register_page, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    path("user_profile/<str:user_id>/", views.user_profile, name="user_profile"),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('users/', views.user_list, name='user_list'),
     path('test-roles/', views.test_roles, name='test_roles'),
    # Autres URLs
]
