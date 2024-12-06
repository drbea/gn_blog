from django.db import models
from django.contrib.auth import get_user_model

from django.utils.timezone import now


User = get_user_model()


class Categorie(models.Model):
    titre = models.CharField(max_length=255)
    # description = models.CharField(max_length=600)

    def __str__(self):
        return self.titre

class Sujet(models.Model):
    titre = models.CharField(max_length=255)


    def __str__(self):
        return self.titre

class Publication(models.Model):
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    contenu = models.TextField(default = "")
    autheur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_update', '-date_creation']

    def __str__(self):
        return self.contenu[:50]  # retourne les 50 premiers caractères

    def count_reactions(self):
        """Retourne un dictionnaire avec le nombre total de chaque type de réaction."""
        return self.reactions.values('type_reaction').annotate(count=models.Count('type_reaction'))


class Commentaire(models.Model):
    autheur = models.ForeignKey(User, on_delete = models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete = models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add = True)
    date_mis_a_jour = models.DateTimeField(auto_now = True)
    contenu = models.TextField(default = "commentaire ici")

    class Meta:
        ordering = ['-date_mis_a_jour', '-date_creation']

    def __str__(self):
        return self.contenu[:50]

# class Reaction(models.Model):
#     autheur = models.ForeignKey(User, on_delete=models.CASCADE)
#     publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
#     commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, blank=True, null=True)
#     type_reaction = models.CharField(max_length=50, choices=[("like", "Like"), ("dislike", "J'aime pas"), ("jadore", "J'adore"),  ("cool", "Cool")])
#     date_reaction = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.utilisateur} a réagi sur {self.publication or self.commentaire} avec {self.type_reaction}"
#

class Reaction(models.Model):
    autheur = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='reactions')
    type_reaction = models.CharField(
        max_length=50,
        choices=[
            ("like", "like"),
            ("jadore", "jadore"),
            ("cool", "cool"),
            ("dislike", "dislike"),
        ]
    )
    date_reaction = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('autheur', 'publication', 'type_reaction')  # Empêche plusieurs réactions du même type par utilisateur/publication

    def __str__(self):
        return f"{self.autheur} a réagi sur {self.publication} avec {self.type_reaction}"




class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    date_creation = models.DateTimeField(default=now)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification pour {self.utilisateur} : {self.message[:50]}"
