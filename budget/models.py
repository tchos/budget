from django.db import models
import datetime, uuid
from datetime import date

from django.core.validators import ValidationError


# Create your models here.
class ExerciceBudgetaire(models.Model):

    # Validator optionnel (si tu veux renforcer la validation personnalisée)
    def validate_annee(value):
        if not isinstance(value, int):
            raise ValidationError("L'année doit être un nombre entier.")

    STATUS_CHOICES = [
        ("provisoire", "Provisoire"),
        ("definitif", "Définitif"),
        ("clos", "Clos")
    ]

    annee = models.IntegerField(unique=True, verbose_name="Année budgétaire", validators=[validate_annee])
    statut = models.CharField(max_length=50, choices=STATUS_CHOICES)

    # Validator pou dire qu'une année budgétaire doit être unique
    def clean(self):
        super().clean()
        # Vérifie si une autre instance avec la même année existe
        if ExerciceBudgetaire.objects.filter(annee=self.annee).exclude(pk=self.pk).exists():
            raise ValidationError({'annee': "Cette année budgétaire existe déjà dans la base de données."})

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
    # Avec related_name='recettes' on pourra accéder à la liste des recettes d'un execice
    exercice = models.ForeignKey('ExerciceBudgetaire', on_delete=models.CASCADE, related_name='recettes')

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
    # Avec related_name='depenses' on pourra accéder à la liste des dépenses d'un execice
    exercice = models.ForeignKey('ExerciceBudgetaire', on_delete=models.CASCADE, related_name='depenses')

    """
    Validation conditionnelle qui affichera une erreur dans le formulaire.
    Pour celà on use la fonction def clean soit dans le models.py soit dans le fichier forms.py
    """
    def clean(self):
        super().clean()
        if (self.montantRealise > self.montantAutorise):
            raise ValidationError("Le montant réalisé ne peut dépasser le montant autorisé !")

        if (self.nature == "fonctionnement" and self.montantRealise > 100):
            # Avec cette methode l'erreur s'affichera au dessus du champs concerné
            raise ValidationError({"montantRealise": ("Les dépenses de fonctionnement ne doivent pas excéder 100")})

    """
    # Avec cette methode l'erreur s'affichera au dessus du champs concerné
    def clean_montantRealise(self):
        if (self.nature == "fonctionnement" and self.montantRealise > 100):
            raise ValidationError("Les dépenses de fonctionnement ne doivent pas excéder 100")
    """

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