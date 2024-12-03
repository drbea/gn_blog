from django.shortcuts import render
from . models import Categorie, Publication, Commentaire, Reaction, Sujet
# Create your views here.

def index(request):
    publication = Publication.objects.all()
    categorie = Categorie.objects.all()

    context = {
        "publications": publication,
        "categories": categorie,
    }
    return render(request, "home/index.html", context)
