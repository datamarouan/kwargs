from django.shortcuts import render

def index(request):
    return render(request, 'page/accueil.html')

def contact(request):
    return render(request, 'page/contact.html')