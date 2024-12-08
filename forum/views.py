# forum/views.py

from django.shortcuts import redirect, render, get_object_or_404
from .models import SujetForum, ForumPost, CategoryPost, Commentaires

# page dacceuil du forum
def acceuil_forum(request):
    sujets = SujetForum.objects.all()
    posts = ForumPost.objects.all()
    categories = CategoryPost.objects.all()
    context = {
        'sujets': sujets,
        "posts": posts,
        "categories": categories,
        }
    # return render(request, 'forum/forum_acceuil.html', context)
    return render(request, 'forum/blog.html', context)

def sujet_forum(request, id_sujet):
    topic = get_object_or_404(SujetForum, pk = id_sujet)
    posts = ForumPost.objects.filter(sujet = topic)

    context = {
        'sujet': topic,
        "posts": posts,
        }
    return render(request, 'forum/forum_acceuil.html', context)



def detail_publication(request, id_publication):

    publication = get_object_or_404(ForumPost, id = id_publication)
    commentaires = publication.commentaires_set.all()
    context = {
        "post": publication,
        "commentaires": commentaires,
        "categories" :CategoryPost.objects.all()

    }
    return render(request, "forum/blog-details.html", context)



## Gestion des commentaire_set
def create_comment(request, id_publication):
    publication = get_object_or_404(ForumPost, id = id_publication)
    if request.method == "POST":
        contenu_commentaire = request.POST.get("commentaire")
        new_commentaire = Commentaires(
            autheur = request.user,
            publication = publication,
            contenu = contenu_commentaire
        )
        new_commentaire.save()

        return redirect("forum:detail_publication", publication.id)
    context = {
    "publication": publication,
    }
    return render(request, "home/post_detail.html", context)



def create_publication(request):
    if request.method == 'POST':
        sujet_id = request.POST.get('sujet')
        category_titre = request.POST.get('category')
        contenu = request.POST.get('contenu')

        sujet = SujetForum.objects.get(id=sujet_id)

        # Vérifie si la catégorie existe déjà
        categorie, created = CategoryPost.objects.get_or_create(titre=category_titre)

        publication = ForumPost(
            sujet=sujet,
            category=categorie,
            contenu=contenu,
            autheur=request.user
        )
        publication.save()

        return redirect('home:index')  # Redirige vers la liste des publications

    context = {
        "sujets": SujetForum.objects.all(),
        "categories": CategoryPost.objects.all(),
    }
    return render(request, 'home/post_create.html', context)
