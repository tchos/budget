from itertools import count

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from budget.models import Recette, Depense, ExerciceBudgetaire
from .forms import ExerciceBudgetaireForm

# For REST API
from django.http import JsonResponse
from budget.serializers import RecetteSerializer, ExerciceSerialier
from rest_framework.response import Response
from rest_framework import generics, status




# Create your views here.

#CBV
class RecetteView(ListView):
    model = Recette
    template_name = "budget/recette.html"
    context_object_name = "recettes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["totalRealise"] = sum(r.montantRealise for r in context['recettes'])
        return context

# FBV
def index(request):
    # return HttpResponse("Bienvenue sur la plateforme du Budget de l'Etat du Cameroun.")
    return render(request, "budget/index.html")

def recette(request):
    return render(request, "budget/recette.html")

# Liste de toutes les dépenses
def depense(request):
    depenses = Depense.objects.all()
    return render(request, "budget/depense.html", {'depenses': depenses})

# On veut afficher les détails d'un exercice
def detail_exercice(request, annee):
    exercice = ExerciceBudgetaire.objects.get(annee=annee)
    print(exercice)
    return render(request, "budget/exercice.html", {'exercice': exercice})

# Enregistrement d'une nouvelle annee budgetaire avec la methode
class ExerciceBudgetaireCreateView(CreateView):
    model = ExerciceBudgetaire
    template_name = 'budget/add_exercice.html'
    form_class = ExerciceBudgetaireForm
    success_message = 'Exercice Budgetaire créé avec succès !!!'
    success_url = reverse_lazy('budget:list_exercice')

    """Validation du formulaire"""

    def form_valid(self, form):
        form.instance.save()
        return super().form_valid(form)

    """
    def form_invalid(self, form):
        print(form.cleaned_data)
        return JsonResponse(form.errors, status=400)
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Enregistrer"
        return context

class ExerciceBudgetaireListView(ListView):
    model = ExerciceBudgetaire
    template_name = "budget/list_exercice.html"
    context_object_name = "exercices"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_exercice"] = ExerciceBudgetaire.objects.all().count()
        return context


class RecetteListAPI(generics.ListCreateAPIView):
    queryset = Recette.objects.all()
    serializer_class = RecetteSerializer

class ExerciceListAPI(generics.ListCreateAPIView):
    queryset = ExerciceBudgetaire.objects.all()
    serializer_class = ExerciceSerialier

    def post(self, request, *args, **kwargs):
        return Response({"detail": "POST method désactivé"}), status.HTTP_405_METHOD_NOT_ALLOWED