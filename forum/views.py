# forum/views.py

from django.shortcuts import redirect, render, get_object_or_404
from .models import SujetForum, ForumPost, CategoryPost, Commentaires

from django.contrib.auth.decorators import login_required

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

# @login_required
def creer_post(request):
    if request.method == "POST":
        # Récupérer ou créer un sujet
        sujet_titre = request.POST.get("sujet_titre", "").strip()
        sujet, _ = SujetForum.objects.get_or_create(
            titre=sujet_titre,
            defaults={"autheur": request.user}
        )

        # Récupérer ou créer les catégories
        categories_titres = request.POST.getlist("categories_titres")
        categories = []
        for titre in categories_titres:
            categorie, _ = CategoryPost.objects.get_or_create(titre=titre.strip())
            categories.append(categorie)

        # Récupérer le contenu et l'image
        contenu = request.POST["contenu"]
        image = request.FILES.get("image")

        # Créer le post
        post = ForumPost.objects.create(
            sujet=sujet,
            auteur=request.user,
            contenu=contenu,
            image=image,
        )
        post.category.set(categories)  # Associer les catégories au post
        post.save()

        return redirect("forum:index")

    # Afficher le formulaire
    sujets = SujetForum.objects.all()
    categories = CategoryPost.objects.all()
    return render(request, "forum/creer_post.html", {"sujets": sujets, "categories": categories})

#
#
# def create_publication(request):
#     if request.method == 'POST':
#         sujet_id = request.POST.get('sujet')
#         category_titre = request.POST.get('category')
#         contenu = request.POST.get('contenu')
#
#         sujet = Sujet.objects.get(id=sujet_id)
#
#         # Vérifie si la catégorie existe déjà
#         categorie, created = Categorie.objects.get_or_create(titre=category_titre)
#
#         publication = Publication(
#             sujet=sujet,
#             category=categorie,
#             contenu=contenu,
#             autheur=request.user
#         )
#         publication.save()
#
#         return redirect('home:index')  # Redirige vers la liste des publications
#
#     context = {
#         "sujets": Sujet.objects.all(),
#         "categories": Categorie.objects.all(),
#         # "conversations": list_messages(request),
#
#     }
#     return render(request, 'home/post_create.html', context)
#
#
# def create_publication(request):
#     if request.method == 'POST':
#         sujet_id = request.POST.get('sujet')
#         category_titre = request.POST.get('category')
#         contenu = request.POST.get('contenu')
#
#         sujet = SujetForum.objects.get(id=sujet_id)
#
#         # Vérifie si la catégorie existe déjà
#         categorie, created = CategoryPost.objects.get_or_create(titre=category_titre)
#
#         publication = ForumPost(
#             sujet=sujet,
#             category=categorie,
#             contenu=contenu,
#             autheur=request.user
#         )
#         publication.save()
#
#         return redirect('home:index')  # Redirige vers la liste des publications
#
#     context = {
#         "sujets": SujetForum.objects.all(),
#         "categories": CategoryPost.objects.all(),
#     }
#     return render(request, 'home/post_create.html', context)
