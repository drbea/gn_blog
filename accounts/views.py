from django.shortcuts import redirect, render
from django.core.mail import EmailMessage, send_mail

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .tokens import account_activation_token
from config import settings


# Create your views here.
User = get_user_model()


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


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)

    context = {
        'user': user
    }
    return render(request, 'accounts/user_profile.html', context)
