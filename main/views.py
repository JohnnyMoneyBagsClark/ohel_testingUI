from django.shortcuts import render

# This function handles requests to the landing page and renders the landingPage.html template
def landing_page(request):
    return render(request, 'main/landingPage.html')
