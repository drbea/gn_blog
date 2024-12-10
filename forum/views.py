# forum/views.py

from django.shortcuts import redirect, render, get_object_or_404
from .models import Reactions, SujetForum, ForumPost, CategoryPost, Commentaires

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# page dacceuil du forum
def acceuil_forum(request):
    search_query = request.POST.get('search-sujet')
    if search_query:
        posts = ForumPost.objects.filter(
            Q(contenu__icontains=search_query) | Q(sujet__titre__icontains= search_query)
        )
        sujets = SujetForum.objects.filter(
            Q(titre__icontains = search_query)
        )
    else:
        posts = ForumPost.objects.all()
        sujets = SujetForum.objects.all()


    categories = CategoryPost.objects.all()
    context = {
        'sujets': sujets,
        "posts": posts,
        "categories": categories,
        }
    # return render(request, 'forum/forum_acceuil.html', context)
    return render(request, 'forum/blog.html', context)

def liste_sujet_forum(request):
    topics = SujetForum.objects.all()
    context = {
        'sujets': topics,
        "categories": CategoryPost.objects.all(),

        }
    return render(request, 'forum/liste_sujet_forum.html', context)

def filtrer_par_categorie(request, id_category):
    category = CategoryPost.objects.get(id = id_category)
    posts = ForumPost.objects.filter(category = category)
    sujets = SujetForum.objects.all()

    context = {
        'sujets': sujets,
        "posts": posts,
        "categories": CategoryPost.objects.all(),
        }
    # return render(request, 'forum/forum_acceuil.html', context)
    return render(request, 'forum/blog.html', context)
    return render(request, "forum/blog.html", context)

def detail_publication(request, id_publication):

    query = request.POST.get("search-sujet")
    if query:
        publications = ForumPost.objects.filter(
            Q(category__titre__icontains = query) |
            Q(contenu__icontains = query)
        )
        sujets = SujetForum.objects.filter(titre__icontains = query)
        # categories = CategoryPost.objects.all()
        context = {
            'sujets': sujets,
            "posts": publications,
            # "categories": categories,
            }

        return render(request, "forum/index", context)

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

def react_to_publication(request, id_publication, reaction_type):
    if not request.user.is_authenticated:
        messages.error(request, 'Vous devez être connecté pour réagir.')
        return redirect('nom_de_votre_page')

    publication = get_object_or_404(ForumPost, id=id_publication)

    # Vérifier si l'utilisateur a déjà réagi à cette publication
    existing_reaction = Reactions.objects.filter(
        autheur=request.user,
        publication=publication
    ).first()

    if existing_reaction:
        if existing_reaction.type_reaction == reaction_type:
            # Si la réaction est la même, on la supprime
            existing_reaction.delete()
            messages.info(request, 'Votre réaction a été supprimée.')
        else:
            # Sinon, mettre à jour avec le nouveau type de réaction
            existing_reaction.type_reaction = reaction_type
            existing_reaction.save()
            messages.success(request, f'Votre réaction a été mise à jour en "{reaction_type}".')
    else:
        # Si aucune réaction n'existe, en créer une nouvelle
        Reactions.objects.create(
            autheur=request.user,
            publication=publication,
            type_reaction=reaction_type
        )
        messages.success(request, f'Vous avez réagi avec "{reaction_type}".')


    return redirect('forum:detail_publication', id_publication=publication.id)

