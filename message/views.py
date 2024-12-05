from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == "POST":
        contenu = request.POST.get("contenu")
        message = Message(sender=request.user, receiver=receiver, contenu=contenu)
        message.save()
        return redirect('message:message', receiver_id = receiver_id)  # Redirige vers la liste des messages

    context = {
        "receiver": receiver,
    }
    return render(request, 'message/send_message.html', context)


@login_required
def messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    received_messages = Message.objects.filter(receiver=request.user, sender=receiver).order_by('timestamp')
    sent_messages = Message.objects.filter(sender=request.user, receiver=receiver).order_by('timestamp')

    # Fusionner les messages reçus et envoyés et les trier par timestamp
    all_messages = sorted(
        list(received_messages) + list(sent_messages),
        key=lambda msg: msg.timestamp
    )

    context = {
        "all_messages": all_messages,
        "receiver": receiver,
    }
    return render(request, 'message/messages.html', context)



@login_required
def conversation_list(request):
    # Récupérer tous les utilisateurs avec lesquels l'utilisateur a des conversations
    users_with_conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    conversations = []
    for user in users_with_conversations:
        last_message = Message.get_last_message_with_user(request.user, user)
        if last_message:
            conversations.append({
                'user': user,
                'last_message': last_message,
            })

    context = {
        'conversations': conversations,
    }
    return render(request, 'message/conversation_list.html', context)






##########################
