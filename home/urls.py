
from django.urls import include, path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name = "index"),
    path("dashboard/", views.dashboard, name = "index"),
    path('post/<int:id_publication>/react/<str:reaction_type>/', views.react_to_publication, name='react_to_publication'),

    path("post/<int:id_publication>/detail/", views.detail_publication, name = "detail_publication"),
    path("post/create/", views.create_publication, name = "create_publication"),
    path("post/<int:id_publication>/update/", views.update_publication, name = "update_publication"),
    path("post/<int:id_publication>/delete/", views.delete_publication, name = "delete_publication"),
    path("post/<int:id_publication>/comment/", views.create_comment, name = "create_comment"),



    path('post/<int:id_publication>/reaction/<str:reaction_type>/', views.add_or_remove_reaction, name='add_reaction'),


]
