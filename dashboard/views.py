from django.shortcuts import render
from django.contrib.auth import get_user_model

from datetime import timedelta
from django.utils import timezone

from forum.models import ForumPost
from home.models import Publication

from . bokeh_graph import bokeh_chart_box, pie_chart_view
User = get_user_model()


def dashboard(request):
    # Calculer la date d'il y a un mois (30 jours)
    one_month_ago = timezone.now() - timedelta(days=30)

    # Filtrer les utilisateurs inscrits depuis cette date
    users_last_month = User.objects.filter(date_joined__gte=one_month_ago).count()

    script, div = bokeh_chart_box()

    piescript, piediv = pie_chart_view()

    context = {
        "users": User.objects.all(),
        "users_last_month": users_last_month,
        "forumpost": ForumPost.objects.all(),
        "publications": Publication.objects.all(),
        "bokeh_script": script,
        "bokeh_div": div,

        "bokeh_pie_script": piescript,
        "bokeh_pie_div": piediv
    }

    return render(request, "dashboard/dashboard.html", context)
