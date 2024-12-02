from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    default_image_link = 'https://cdn3.iconfinder.com/data/icons/web-design-and-development-2-6/512/87-1024.png'
    user_avatar = models.CharField(max_length = 500, null= True, blank= True, default = default_image_link)

    
