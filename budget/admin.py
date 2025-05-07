from django.contrib import admin
from .models import *
import math

# Personnalisation de l'interface d'administration

# Personnalisation de l'affichage des Recettes
class RecetteAdmin(admin.ModelAdmin):
    # 1. Afficher plus de champs dans les listes (list_display)
    list_display = ('imputation', 'nom', 'exercice', 'categorie', 'montantAutorise', 'montantRealise', 'tauxDeRealisation')
    # 2. Activer la recherche (search_fields)
    search_fields = ('exercice__annee', 'nom', 'categorie')
    # 3. Filtres sur la colonne de droite (list_filter)
    list_filter = ('categorie', 'exercice')

    # 4. Formulaire organisé en sections (fieldsets)
    fieldsets = (
        ('Informations principales', {
            'fields': ('imputation', 'nom', 'categorie')
        }),
        ('Contexte budgétaire', {
            'fields': ('exercice', 'montantPrevu', 'montantAutorise', 'montantRealise')
        }),
    )

    # 5. Ajout de champs calculés dans list_display
    def tauxDeRealisation(self, obj):
        if obj.montantAutorise != 0:
            return f"{'%.2f' % (100 * obj.montantRealise / obj.montantAutorise)} %"
        else:
            return 'n/a'

    tauxDeRealisation.short_description = "Taux de réalisation"


# Personnalisation de l'affichage des Dépenses
class DepenseAdmin(admin.ModelAdmin):
    # 1. Afficher plus de champs dans les listes (list_display)
    list_display = ('chapitre', 'nature', 'fonction', 'exercice', 'montantAutorise', 'montantRealise', 'tauxDeRealisation')
    # 2. Activer la recherche (search_fields)
    search_fields = ('exercice__annee', 'chapitre', 'nature')
    # 3. Filtres sur la colonne de droite (list_filter)
    list_filter = ('chapitre', 'exercice', 'nature')

    # 4. Formulaire organisé en sections (fieldsets)
    fieldsets = (
        ('Informations principales', {
            'fields': ('chapitre', 'nature', 'paragraphe', 'fonction')
        }),
        ('Contexte budgétaire', {
            'fields': ('exercice', 'montantPrevu', 'montantAutorise', 'montantRealise')
        }),
    )

    # 5. Ajout de champs calculés dans list_display
    def tauxDeRealisation(self, obj):
        if obj.montantAutorise != 0:
            return f"{'%.2f' % (100 * obj.montantRealise / obj.montantAutorise)} %"
        else:
            return 'n/a'

    tauxDeRealisation.short_description = "Taux de réalisation"

"""
Les Inlines (édition d’objets liés dans une même page)
Ex. : Ajouter les Dépenses directement dans l’admin d’un ExerciceBudgétaire
"""
class DepenseInline(admin.TabularInline):
    model = Depense
    extra = 1

"""
Les Inlines (édition d’objets liés dans une même page)
Ex. : Ajouter les Recettes directement dans l’admin d’un ExerciceBudgétaire
"""
class RecetteInline(admin.TabularInline):
    model = Recette
    extra = 1

class ExerciceBudgetaireAdmin(admin.ModelAdmin):
    inlines = [DepenseInline, RecetteInline]


# Register your models here.
admin.site.register(ExerciceBudgetaire, ExerciceBudgetaireAdmin)
admin.site.register(Recette, RecetteAdmin)
admin.site.register(Depense, DepenseAdmin)
admin.site.register(Person)
