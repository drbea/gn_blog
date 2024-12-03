from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=600)

    def __str__(self):
        return self.nom

class Sujet(models.Model):
    titre = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    # utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Publication(models.Model):
    contenu = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mis_a_jour = models.DateTimeField(auto_now=True)
    jaime = models.ManyToManyField(User, related_name='like')
    jaime_pas = models.ManyToManyField(User, related_name='dislike')

    class Meta:
        ordering = ['-date_mis_a_jour', '-date_creation']

    def __str__(self):
        return self.contenu[:50]  # retourne les 50 premiers caractères

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mis_a_jour = models.DateTimeField(auto_now=True)
    contenu = models.CharField(max_length=200, default='Contenu par défaut')
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')
    class Meta:
        ordering = ['-date_mis_a_jour', '-date_creation']

    def __str__(self):
        return self.contenu
class Reaction(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, blank=True, null=True)
    type_reaction = models.CharField(max_length=50, choices=[('like', 'Like'), ('dislike', 'Dislike')])
    date_reaction = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur} a réagi sur {self.publication or self.commentaire} avec {self.type_reaction}"

