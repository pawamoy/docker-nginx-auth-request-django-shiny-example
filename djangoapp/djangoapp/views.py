from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import requests

from bs4 import BeautifulSoup

from .forms import SignUpForm


def home(request):
    return render(request, 'djangoapp/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'djangoapp/signup.html', {'form': form})


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
    soup = BeautifulSoup(response.content, 'html.parser')
    return JsonResponse({'html_contents': str(soup)})


def auth(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    return HttpResponse(status=403)
