from django.contrib import admin
from  .models import Categorie, Commentaire, Publication, Reaction, Sujet
# Register your models here.

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    pass

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    pass

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    pass

@admin.register(Sujet)
class sujetnAdmin(admin.ModelAdmin):
    pass
