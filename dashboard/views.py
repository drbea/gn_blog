from django.shortcuts import render
from django.contrib.auth import get_user_model

from datetime import timedelta
from django.utils import timezone

from forum.models import ForumPost
from home.models import Publication
User = get_user_model()


def dashboard(request):

    # Calculer la date d'il y a un mois (30 jours)
    one_month_ago = timezone.now() - timedelta(days=30)

    # Filtrer les utilisateurs inscrits depuis cette date
    users_last_month = User.objects.filter(date_joined__gte=one_month_ago).count()

    # Create your views here.
    context = {
        "users": User.objects.all(),
        "users_last_month": users_last_month,
        "forumpost": ForumPost.objects.all(),
        "publications": Publication.objects.all(),
    }

    return render(request, "dashboard/dashboard.html", context)