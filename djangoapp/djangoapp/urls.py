"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('admin/', admin.site.urls),

    path('signin/', auth_views.LoginView.as_view(), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('signup/', views.signup, name='signup'),

    path('shiny/', views.shiny, name='shiny'),
    path('shiny_contents/', views.shiny_contents, name='shiny_contents'),
    path('shiny_auth/', views.auth, name='shiny_auth'),
]
