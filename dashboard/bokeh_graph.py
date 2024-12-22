from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import WheelZoomTool, ColumnDataSource
from home.models import  Categorie, Publication, Commentaire, Reaction, Sujet, Notification
from forum.models import Reactions, SujetForum, ForumPost, CategoryPost, Commentaires

blog = {
    "elements": ["publications", "commentaires", "Reactions", "Notification"],
    "counts": [Publication.objects.all().count(), Commentaire.objects.all().count(), Reaction.objects.all().count(), Notification.objects.all().count()]

}


def bokeh_chart_box():
    source = ColumnDataSource(data = {"elements": blog["elements"], "counts": blog["counts"] })
    # creation d'un graphique
    plot = figure(
        x_range = blog["elements"],
        # toolbar = None,
        title = "Representation des elements",
        x_axis_label = "elements du blog",
        y_axis_label = "quantite",
        toolbar_location = None,
        tools = ""
        )
    plot.vbar(x = "elements", top = "counts", width = .8, source = source)


    script, div = components(plot)
    # show(plot)
    return script, div





categories_forum = [cat.titre for cat in CategoryPost.objects.all()]
post_forum = [ForumPost.objects.filter(category__titre__icontains =cat).count() for cat in categories_forum]
forum = {
    "categories": categories_forum,
    "post": post_forum,
    }

# from bokeh.plotting import figure
# from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from math import pi
import pandas as pd

def pie_chart_view():

    # Transformation des données pour un diagramme circulaire
    # data = pd.DataFrame({'category': categories_forum, 'value': post_forum})
    data = pd.DataFrame(forum)

    data['angle'] = data['post'] / data['post'].sum() * 2 * pi
    data['color'] = Category20c[len(data)]  # Palette de couleurs dynamique

    # Création de la figure
    p = figure(height=350, title="Répartition des posts par catégorie", toolbar_location=None,
               tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0))

    # Ajout des portions du diagramme
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='category', source=data)
    p.text(
        x=0.5, y=0.5,  # Position des étiquettes (centrée par défaut)
        text='category',  # Le texte est le nom de chaque catégorie
        source=data,  # Source des données pour les étiquettes
        angle=cumsum('angle', include_zero=True),# + data['angle'] / 2,  # Position des étiquettes sur les angles
        text_align='center',  # Centrer les étiquettes
        text_baseline='middle',  # Centrer verticalement les étiquettes
        color='white',  # Couleur des étiquettes
    )
    # Configuration du graphique
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # Génération des composants Bokeh
    script, div = components(p)
    return script, div
