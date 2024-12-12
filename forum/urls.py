from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.acceuil_forum, name = "index"),
    path("sujets/", views.liste_sujet_forum, name = "liste_sujet_forum"),
    path("detail_publication/<int:id_publication>/", views.detail_publication, name = "detail_publication"),
    path("delete_publication/<int:id_publication>/", views.delete_publication, name = "delete_publication"),
    path("delete_comment/<int:id_commentaire>/", views.delete_comment, name = "delete_comment"),
    path("post/create/", views.creer_post, name = "create_post"),
    path("post/<int:id_publication>/comment/", views.create_comment, name = "create_comment"),
    path("post/<int:id_category>/filtrer_par_categorie/", views.filtrer_par_categorie, name = "filtrer_par_categorie"),
    path('post/<int:id_publication>/react/<str:reaction_type>/', views.react_to_publication, name='react_to_publication'),

]
# react_to_publication
