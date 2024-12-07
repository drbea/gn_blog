from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.acceuil_forum, name = "index"),
    path("sujet/<int:in_sujet>", views.sujet_forum, name = "sujet"),
    path("detail_publication/<int:id_publication>/", views.detail_publication, name = "detail_publication"),
    path("post/<int:id_publication>/comment/", views.create_comment, name = "create_comment")
]
