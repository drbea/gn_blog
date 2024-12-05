from django.shortcuts import render, get_object_or_404, redirect
from . models import Categorie, Publication, Commentaire, Reaction, Sujet

from message.models import Message
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your views here.

def list_messages(request):
    # Récupérer tous les utilisateurs avec lesquels l'utilisateur a des conversations
    users_with_conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    conversations = []
    for user in users_with_conversations:
        last_message = Message.get_last_message_with_user(request.user, user)
        if last_message:
            conversations.append({
                'user': user,
                'last_message': last_message,
            })
    return conversations

## Gestion des publoications
def index(request):
    publication = Publication.objects.all()
    categorie = Categorie.objects.all()

    context = {
        "publications": publication,
        "categories": categorie,
        "conversations": list_messages(request),
    }
    return render(request, "home/index.html", context)

def detail_publication(request, id_publication):

    publication = get_object_or_404(Publication, id = id_publication)
    commentaires = publication.commentaire_set.all()
    context = {
        "publication": publication,
        "post": publication,
        "commentaires": commentaires,
        "comments": commentaires,
        "conversations": list_messages(request),

    }
    return render(request, "home/post_detail.html", context)


def create_publication(request):
    if request.method == 'POST':
        sujet_id = request.POST.get('sujet')
        category_titre = request.POST.get('category')
        contenu = request.POST.get('contenu')

        sujet = Sujet.objects.get(id=sujet_id)

        # Vérifie si la catégorie existe déjà
        categorie, created = Categorie.objects.get_or_create(titre=category_titre)

        publication = Publication(
            sujet=sujet,
            category=categorie,
            contenu=contenu,
            autheur=request.user
        )
        publication.save()

        return redirect('home:index')  # Redirige vers la liste des publications

    context = {
        "sujets": Sujet.objects.all(),
        "categories": Categorie.objects.all(),
        "conversations": list_messages(request),

    }
    return render(request, 'home/post_create.html', context)

def update_publication(request, id_publication):
    publication = get_object_or_404(Publication, id = id_publication)

    if request.method == 'POST':
        sujet_id = request.POST.get('sujet')
        category_titre = request.POST.get('category')
        contenu = request.POST.get('contenu')
        sujet = Sujet.objects.get(id=sujet_id)

        # Vérifie si la catégorie existe déjà
        categorie, created = Categorie.objects.get_or_create(titre=category_titre)
        publication.sujet=sujet
        publication.category=categorie
        publication.contenu=contenu
        publication.save()
        return redirect('home:detail_publication', id=publication.id)  # Redirige vers la page de détail de la publication

    commentaires = publication.commentaire_set.all()
    context = {
        "publication": publication,
        "conversations": list_messages(request),
        "sujets": Sujet.objects.all(),
        "categories": Categorie.objects.all()
        }
    return render(request, 'home/post_update.html', context)


def delete_publication(request, id_publication):
    publication = get_object_or_404(Publication, id = id_publication)
    if request.method == "POST":
        publication.delete()
        return redirect("home:index")

    context = {
        "publication": publication,
        "conversations": list_messages(request),

        }
    return render(request, 'home/post_delete.html', context)

## Gestion des commentaire_set
def create_comment(request, id_publication):
    publication = get_object_or_404(Publication, id = id_publication)
    if request.method == "POST":
        contenu_commentaire = request.POST.get("commentaire")
        new_commentaire = Commentaire(
            autheur = request.user,
            publication = publication,
            contenu = contenu_commentaire
        )
        new_commentaire.save()
        return redirect("home:detail_publication", publication.id)
    context = {
    "publication": publication,
    "conversations": list_messages(request),

    }
    return render(request, "home/post_detail.html", context)


def detail_comment(request, id_commentaire):
    commentaire = get_object_or_404(Commentaire, id = id_commentaire)
    context = {
        "commentaires": commentaire,
        "comments": commentaire,
        "conversations": list_messages(request),
    }
    return render(request, "home/post_detail.html", context)



def delete_comment(request, id_commentaire):
    commentaire = get_object_or_404(Commentaire, id = id_commentaire)
    if request.method == "POST":
        commentaire.delete()
        return redirect("home:index")

    context = {
        "publication": publication,
        "commentaire": commentaire
        }
    return render(request, 'home/post_delete.html', context)
