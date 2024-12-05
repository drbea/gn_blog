from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    contenu = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
        
    @staticmethod
    def get_last_message_with_user(user1, user2):
        return Message.objects.filter(
            (models.Q(sender=user1) & models.Q(receiver=user2)) |
            (models.Q(sender=user2) & models.Q(receiver=user1))
        ).order_by('-timestamp').first()
