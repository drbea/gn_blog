# forum/models.py

from django.db import models
from django.contrib.auth import get_user_model

from django.utils.timezone import now

User = get_user_model()

class SujetForum(models.Model):
    titre = models.CharField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    autheur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class CategoryPost(models.Model):
    titre = models.CharField(max_length=255)

    def __str__(self):
        return self.titre



class ForumPost(models.Model):
    category = models.ManyToManyField(CategoryPost, related_name="categorie")
    sujet = models.ForeignKey(SujetForum, related_name="posts", on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    image = models.ImageField(upload_to="media/forum", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.auteur.username} in {self.sujet.titre}"


class Commentaires(models.Model):
    autheur = models.ForeignKey(User, on_delete = models.CASCADE)
    publication = models.ForeignKey(ForumPost, on_delete = models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add = True)

    contenu = models.TextField(default = "commentaire ici")

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return self.contenu[:50]


class Reactions(models.Model):
    autheur = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(ForumPost, on_delete=models.CASCADE) #, related_name='reactions')
    type_reaction = models.CharField(
        max_length=50,
        choices=[
            ("jaime", "Like"),
            ("dislike", "Dislike"),
        ]
    )
    date_reaction = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('autheur', 'publication', 'type_reaction')  # Empêche plusieurs réactions du même type par utilisateur/publication

    def __str__(self):
        return f"{self.autheur} a réagi sur {self.publication} avec {self.type_reaction}"
