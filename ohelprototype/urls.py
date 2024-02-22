#ohelprototype/urls.py

from django.contrib import admin
from django.urls import path, include 
from main import views as main_views  

urlpatterns = [
    path('', main_views.landing_page, name='landing_page'),  
]
