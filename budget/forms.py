from django import forms
from .models import ExerciceBudgetaire

class ExerciceBudgetaireForm(forms.ModelForm):
    class Meta:
        model = ExerciceBudgetaire
        fields = ['annee','statut']

        labels = {
            'annee': 'Année budgétaire',
            'statut': 'Statut',
        }

        widgets = {
            'annee' : forms.NumberInput(attrs={'class':'form-control'}),
            'statut' : forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned_data = super(ExerciceBudgetaireForm, self).clean()
        annee = cleaned_data.get('annee')
        statut = cleaned_data.get('statut')

        if not str(annee).isdigit():
            raise forms.ValidationError({"annee": "L' année budgétaire ne doit contenir que des chiffres !!!"})