#views.py
from django.shortcuts import render

# This function handles requests to the landing page and renders the landingPage.html template
def landing_page(request):
    return render(request, 'main/landingPage.html')

def chatbot(request):
    return render(request, 'main/chatbot.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def contact(request):
    return render(request, 'main/contact.html')

def signup(request):
    return render(request, 'main/signup.html')

def download(request):
    return render(request, 'main/download.html')