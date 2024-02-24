# ohelprototype/urls.py

from django.contrib import admin
from django.urls import path, include 
from main import views as main_views  # Import views from the 'main' app

urlpatterns = [
    path('', main_views.landing_page, name='landing_page'),  
    path('chatbot/', main_views.chatbot, name='chatbot'),  
    path('about-us/', main_views.about_us, name='about_us'),
    path('contact/', main_views.contact, name='contact'),
    path('signup/', main_views.signup, name='signup'),
    path('download/', main_views.download, name='download'),
]
