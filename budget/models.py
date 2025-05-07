from django.db import models
import datetime, uuid
from datetime import date

from django.core.validators import ValidationError


# Create your models here.
class ExerciceBudgetaire(models.Model):
    STATUS_CHOICES = [
        ("provisoire", "Provisoire"),
        ("definitif", "Définitif"),
        ("clos", "Clos")
    ]

    annee = models.IntegerField()
    statut = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.annee}"

# Modèle Recette
class Recette(models.Model):
    CATEGORIE_CHOICES = [
        ("fiscale", "Fiscale"),
        ("douanière", "Douanière"),
        ("dons", "Dons"),
        ("emprunts", "Emprunts"),
        ("autres", "Autres"),
    ]

    imputation = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    montantPrevu = models.IntegerField()
    montantAutorise = models.IntegerField()
    montantRealise = models.IntegerField()
    exercice = models.ForeignKey('ExerciceBudgetaire', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} + {self.montantPrevu} FCFA"

#Modèle Dépense
class Depense(models.Model):
    NATURE_CHOICES = [
        ("fonctionnement", "Fonctionnement"),
        ("investissement", "Investissement"),
    ]

    FONCTION_CHOICES = [
        ("souveraineté", "Souveraineté"),
        ("santé", "Santé"),
        ("sécurité", "Sécurité"),
    ]

    chapitre = models.CharField(max_length=100)
    nature = models.CharField(max_length=50, choices=NATURE_CHOICES)
    paragraphe = models.CharField(max_length=100)
    fonction = models.CharField(max_length=50, choices=FONCTION_CHOICES)
    montantPrevu = models.IntegerField()
    montantAutorise = models.IntegerField()
    montantRealise = models.IntegerField()
    exercice = models.ForeignKey('ExerciceBudgetaire', on_delete=models.CASCADE)

    """
    Validation conditionnelle qui affichera une erreur dans le formulaire.
    Pour celà on use la fonction def clean soit dans le models.py soit dans le fichier forms.py
    """
    def clean(self):
        super().clean()
        if (self.montantRealise > self.montantAutorise):
            raise ValidationError("Le montant réalisé ne peut dépasser le montant autorisé !")

    # Avec cette methode l'erreur s'affichera sous le champs concerné
    def clean_montantRealise(self):
        if (self.nature == "fonctionnement" and self.montantRealise > 100):
            raise ValidationError("Les dépenses de fonctionnement ne doivent pas excéder 100")

    def __str__(self):
        return f"{self.chapitre} - {self.montantPrevu} FCFA"


# Modèle Personne
class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de la personne",max_length=32)
    prenom = models.CharField("Prénom de la personne", max_length=32)
    datenais = models.DateField("Date de naissance")

    def __str__(self):
        age = date.today().year - self.datenais.year
        return f"Nom: {self.nom} - Age: {age} ANS"