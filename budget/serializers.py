from rest_framework import serializers
from.models import *

class RecetteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recette
        fields = '__all__'

class ExerciceSerialier(serializers.ModelSerializer):
    class Meta:
        model = ExerciceBudgetaire
        fields = '__all__'