from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    default_image_link = 'https://cdn3.iconfinder.com/data/icons/web-design-and-development-2-6/512/87-1024.png'
    profile_pick = models.ImageField(upload_to="", null=True, blank=True, default="avatar.svg")
    default_avatar = models.CharField(max_length=500, null=True, blank=True, default=default_image_link)
    bio = models.TextField(null=True, blank=True, default="Je suis Mr/Mme ...")
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        help_text="Role of the user: admin, moderator, or user."
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin_or_moderator(self):
        return self.role in ['admin', 'moderator']


class Followers(models.Model):
    followers = models.ForeignKey(User, related_name="Following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="Followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("followers", "followed")

    def __str__(self):
        return f"{self.followers.username} follows {self.followed.username}"


# class Followers(models.Model):
#     followers = models.ForeignKey(User, related_name = "Following", on_delete = models.CASCADE)
#     followed = models.ForeignKey(User, related_name = "Followers", on_delete = models.CASCADE)
#     created = models.DateTimeField(auto_now_add = True)

#     class Meta:
#         unique_together = ("followers", "followed")

#     def __str__(self):
#         return f"{self.followers.username} follows {self.followed.username}"
