from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from budget.models import Recette


# Create your views here.

#CBV
class RecetteView(ListView):
    model = Recette
    template_name = "recette.html"
    context_object_name = "recettes"

    def get_context_data(self, **kwargs):
        context = super(RecetteView, self).get_context_data(**kwargs)
        context["totalRealise"] = sum(
            r.montantRealise for r in context['recette_list']
        )
        return context

# FBV
def index(request):
    # return HttpResponse("Bienvenue sur la plateforme du Budget de l'Etat du Cameroun.")
    return render(request, "index.html")

def recette(request):
    return render(request, "recette.html")

def depense(request):
    return render(request, "depense.html")
