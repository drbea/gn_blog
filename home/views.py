from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from . models import Categorie, Publication, Commentaire, Reaction, Sujet, Notification
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from message.models import Message
from django.contrib.auth import get_user_model #, logout
from django.db.models import Q

User = get_user_model()
# Create your views here.

def list_messages(request):
    # Récupérer tous les utilisateurs avec lesquels l'utilisateur a des conversations
    users_with_conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    conversations = []
    if users_with_conversations:
        for user in users_with_conversations:
            last_message = Message.get_last_message_with_user(request.user, user)
            if last_message:
                conversations.append({
                    'user': user,
                    'last_message': last_message,
                })
    return conversations


def liste_notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')

    notifications = request.user.notifications.all()  # Notifications pour l'utilisateur connecté
    return render(request, 'home/liste_notifications.html', {'notifications': notifications})


## Gestion des publoications
# @login_required
def index(request):
    publication = Publication.objects.all()
    categorie = Categorie.objects.all()
    conversations =  list_messages(request) if request.user.is_authenticated else None,

    context = {
        "publications": publication,
        "categories": categorie,
        "conversations": conversations,
    }
    return render(request, "home/index_blog.html", context)

def detail_publication(request, id_publication):

    publication = get_object_or_404(Publication, id = id_publication)
    commentaires = publication.commentaire_set.all()
    conversations =  list_messages(request) if request.user.is_authenticated else None,

    context = {
        "publication": publication,
        "post": publication,
        "commentaires": commentaires,
        "comments": commentaires,
        "conversations": conversations,
    }
    return render(request, "home/post_detail.html", context)


def create_publication(request):
    if not  request.user.is_admin_or_moderator():
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de creer un article.")
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
    if request.user.is_admin_or_moderator():
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de mettre ajour un article.")

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
    if request.user.is_admin_or_moderator():
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de supprimer un article.")
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


        # Ajouter une notification
        Notification.objects.create(
            utilisateur=publication.autheur,  # L'utilisateur qui recevra la notification
            message=f"{request.user.username} a commente la publication <b>{publication.contenu[:20]}</b>."
        )

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
    if request.user.is_admin_or_moderator():
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de supprimer un commentaire.")
    commentaire = get_object_or_404(Commentaire, id = id_commentaire)
    if request.method == "POST":
        commentaire.delete()
        return redirect("home:index")

    context = {
        # "publication": publication,
        "commentaire": commentaire
        }
    return render(request, 'home/post_delete.html', context)




# @login_required
# def add_or_remove_reaction(request, id_publication, reaction_type):
#     publication = get_object_or_404(Publication, id=id_publication)
#     user = request.user
#
#     # Vérifiez si l'utilisateur a déjà réagi à cette publication
#     reaction, created = Reaction.objects.get_or_create(
#         autheur=user,
#         publication=publication,
#         defaults={'type_reaction': reaction_type}
#     )
#
#     if not created:
#         # Si l'utilisateur a déjà réagi, mettez à jour la réaction
#         if reaction.type_reaction == reaction_type:
#             # Si la réaction est déjà du même type, supprimez-la
#             reaction.delete()
#         else:
#             # Sinon, mettez à jour la réaction
#             reaction.type_reaction = reaction_type
#             reaction.save()
#     else:
#         # Si l'utilisateur n'a pas encore réagi, créez une nouvelle réaction
#         reaction.type_reaction = reaction_type
#         reaction.save()
#
#     return redirect('home:detail_publication', id_publication=id_publication)




####################

def react_to_publication(request, id_publication, reaction_type):
    if not request.user.is_authenticated:
        messages.error(request, 'Vous devez être connecté pour réagir.')
        return redirect('nom_de_votre_page')

    publication = get_object_or_404(Publication, id=id_publication)

    # Vérifier si l'utilisateur a déjà réagi à cette publication
    existing_reaction = Reaction.objects.filter(
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
        Reaction.objects.create(
            autheur=request.user,
            publication=publication,
            type_reaction=reaction_type
        )
        messages.success(request, f'Vous avez réagi avec "{reaction_type}".')

    # Ajouter une notification
    Notification.objects.create(
        utilisateur=publication.autheur,  # L'utilisateur qui recevra la notification
        message=f"{request.user.username} a réagi à votre publication avec {reaction_type}."
    )

    return redirect('home:detail_publication', id_publication=publication.id)


def dashboard(request):
    if request.user.is_admin_or_moderator():
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de voir le tableau de bord.")

    context = {}
    return render(request, "home/dashboard.html", context)

def categories(request,id_category):

    categorie = get_object_or_404(Categorie, id = id_category)
    posts = Publication.objects.filter(category = categorie)
    categories = Categorie.objects.all()

    context = {
        "publications": posts,
        "categories": categories
    }
    return render(request, "home/index_blog.html", context)

def index_blog (request):
    posts = Publication.objects.all()
    categories = Categorie.objects.all()

    context = {
        "publications": posts,
        "categories": categories
    }
    return render(request, "home/index_blog.html",context)

def blog_Publication(request):
    posts = Publication.objects.all()
    categories = Categorie.objects.all()

    context = {
        "publications": posts,
        "categories": categories
    }
    return render(request, "home/detailpublication.html",context)
