from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Bienvenue sur la plateforme du Budget de l'Etat du Cameroun.")

def recettes(request):
    return HttpResponse("Bienvenue sur la page des recettes")

def depenses(request):
    return HttpResponse("Bienvenue sur la page des Dépenses")
