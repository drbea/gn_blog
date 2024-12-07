from django.contrib import admin
from . models import CategoryPost, ForumPost, Commentaires, Reactions, SujetForum
# Register your models here.


@admin.register(CategoryPost)
class CategoryPostAdmin(admin.ModelAdmin):
    pass


@admin.register(SujetForum)
class SujetForumAdmin(admin.ModelAdmin):
    pass


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    pass


@admin.register(Commentaires)
class CommentairesAdmin(admin.ModelAdmin):
    pass


@admin.register(Reactions)
class ReactionsAdmin(admin.ModelAdmin):
    pass