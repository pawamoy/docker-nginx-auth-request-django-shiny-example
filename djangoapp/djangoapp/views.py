from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import requests

from bs4 import BeautifulSoup

from cerberus_ac.models import RolePrivilege

from .forms import SignUpForm
from .models import User
from .tokens import account_activation_token


def home(request):
    return render(request, 'djangoapp/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.add_message(request, messages.INFO, user.email)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'djangoapp/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # user.is_active = True
        user.email_confirmed = True
        user.save()
        # login(request, user)
        messages.add_message(
            request, messages.INFO,
            'Your email has been confirmed. Please wait for an '
            'administrator to activate your account.',
            extra_tags='alert-info')
        # notify admin to activate account
        return redirect('home')

    return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def about(request):
    return render(request, 'djangoapp/about.html')


def contact(request):
    return render(request, 'djangoapp/contact.html')


@login_required
def shiny(request):
    return render(request, 'djangoapp/shiny.html')


@login_required
def shiny_contents(request):
    response = requests.get('http://shinyapp:8100')
    soup = BeautifulSoup(response.content, "html.parser")
    return JsonResponse({'html_contents': str(soup)})


def auth(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    return HttpResponse(status=403)


@login_required
def activate_user_account(request, user_id):
    if not request.user.is_staff:
        pass  # raise error or else

    user_to_activate = User.objects.get(id=user_id)
    if user_to_activate.is_active:
        pass  # handle case

    if not user_to_activate.email_confirmed:
        pass  # handle case

    user_to_activate.is_active = True
    user_to_activate.save()

    # notify user that the account has been activated

    return redirect('admin')
