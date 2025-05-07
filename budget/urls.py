from django.urls import path
from . import views
import inspect
from .views import RecetteView

"""
urlpatterns = [
    path('', views.index, name='index'),
    #path('recettes/', views.recettes, name='recettes'),
    #path('depenses/', views.depenses, name='depenses'),
]
"""

app_name = 'budget'

# Initialisation de la variable path qui contiendra la liste des path
urlpatterns = [
    path('', views.index, name='index'),
    path('recettes/', RecetteView.as_view(), name='recette_list'),
]

# Inspecter les fonctions définies dans views
for name, func in inspect.getmembers(views, inspect.isfunction):
    if func.__module__ == views.__name__:
        urlpatterns.append(
            path(name + '/', func, name=name)
        )