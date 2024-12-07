from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import EmailMessage, send_mail

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .tokens import account_activation_token
from . models import Followers
from config import settings

from django.http import HttpResponseForbidden

def logout_suer(request):
    logout(request)
    return HttpResponse("<p class='bg-sucess text-center'> deconnection effctué avec succès .. </p>")


# Create your views here.
User = get_user_model()

def test_roles(request):
    # Exemple : Vérification des rôles
    admin_user = User.objects.get(username="admin_user")
    if admin_user.role == User.ADMIN:
        return HttpResponse("Cet utilisateur est un admin.")
    else:
        return HttpResponse("Cet utilisateur n'est pas un admin.")

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect("accounts:register")

        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters')
            return redirect("accounts:register")

        if password == password2:
            if not username.isalnum():
                messages.error(request, 'Username must be alpha numeric')
                return redirect("accounts:register")

            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_active = False
            new_user.save()

            current_site = get_current_site(request)
            email_subject = 'Welcome to GN-BLOG - Activate Your Account'
            message = render_to_string('accounts/email_confirmation.html', {
                'name': new_user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_user.email,]
            email = EmailMessage(email_subject, message, email_from, recipient_list)
            email.fail_silently = True
            try:
                email.send()
                print('email sent')
            except Exception as e:
                print(e, "email not sent")

            messages.success(request, 'Your account has been created successfully. We have sent you a confirmation email, please confirm your email address to activate your account.')

            return redirect('accounts:login')
        else:
            messages.error(request, 'Password not matched')
        print(request.POST)
    return render(request, 'accounts/register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and account_activation_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        messages.success(request, 'Your account has been activated')
        return redirect('home:index')
    else:
        messages.error(request, 'Activation link is invalid')
        return render(request, 'accounts/activation_invalide.html')


def login_page(request):
    if request.user.is_authenticated:
        return render(request, 'home/index.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'Login Successful')
            login(request, user)
            return render(request, 'home/index.html')
        else:
            messages.error(request, 'Invalid credentials please try again')
    return render(request, 'accounts/login_page.html')

# Gestion des Followers
# @login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = Followers.objects.filter(followed=user)
    following = Followers.objects.filter(followers=user)

    context = {
        "user": user,
        "followers": followers,
        "followings": following,
    }
    return render(request, 'accounts/user_profile.html', context)

# @login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        follow, created = Followers.objects.get_or_create(followers=request.user, followed=user_to_follow)
        if not created:
            follow.delete()
            print(f"Vous suivez ne plus  {user_to_follow.username}.")
        else:
            print(f"Vous suivez desormais  {user_to_follow.username}.")
        return redirect('accounts:user_list')  # Redirige vers la liste des utilisateurs

    return redirect('accounts:user_list')  # Redirige vers la liste des utilisateurs

def user_list(request):
    users = User.objects.all()
    following_status = {}

    if request.user.is_authenticated:
        for user in users:
            following_status[user.id] = Followers.objects.filter(followers=request.user, followed=user).exists()

    return render(request, 'accounts/user_list.html', {'users': users, 'following_status': following_status})


def test_roles(request):
    if request.user.role == User.ADMIN:
        return HttpResponse("Bienvenue, Admin !")
    elif request.user.role == User.MODERATOR:
        return HttpResponse("Bienvenue, Modérateur !")
    elif request.user.role == User.USER:
        return HttpResponse("Bienvenue, Utilisateur !")
    else:
        return HttpResponse("Rôle inconnu.")

def admin_view(request):
    if request.user.role != User.ADMIN:
        return HttpResponseForbidden("Access denied. Admins only.")
    # Logic for admin view
    return render(request, 'admin_page.html')
