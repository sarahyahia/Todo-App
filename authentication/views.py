from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes, force_str, force_text
from .utils import generate_token
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import threading



class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()




################### send activation mail ######################
def send_activation_email(user, request):
    current_site = get_current_site(request)
    ######################### send mail with email template ####################################
    htmly = get_template('authentication/Email.html')
    context = {
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    subject, from_email,to = 'Activate your account', settings.EMAIL_HOST_USER, user.email
    html_content = htmly.render(context)
    email = EmailMultiAlternatives(subject, html_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")

    if not settings.TESTING:
        EmailThread(email).start()


@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,'Password should be at least 6 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,'Passwords mismatched')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,'Username is taken, choose another one')
            context['has_error'] = True

            return render(request, 'authentication/register.html', context, status=409) # to make sure the status code returned in tests/test_views.py is right

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'authentication/register.html', context, status=409) # to make sure the status code returned in tests/test_views.py is right

        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        send_activation_email(user, request)
        messages.add_message(request, messages.SUCCESS,'We sent you an email to verify your account, check your inbox.')
        return redirect('login')
    return render(request, 'authentication/register.html')


@auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username= username, password= password)
        
        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,'Email is not verified, please check your email inbox')
            return render(request, 'authentication/login.html', context, status=401)
        
        if not user:
            messages.add_message(request, messages.ERROR,'wrong user or password')
            return render(request, 'authentication/login.html', context, status=401)
        
        login(request, user)
        messages.add_message(request, messages.SUCCESS,f'Welcome {user.username}')
        return redirect(reverse('home'))
        
    return render(request, 'authentication/login.html')



def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,'Logged out successfully')
    return redirect(reverse('login'))



def activate_user (request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user,token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,'Email has been verified, you can now login')
        return redirect(reverse('login'))
    
    messages.add_message(request, messages.SUCCESS,'expired link , do you want to resend another one')
    return redirect(reverse('login'))