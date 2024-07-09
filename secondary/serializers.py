from rest_framework import serializers
from .models import NameOfGrades, AdministratorTypes, NamesOfOlympia

class NameOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameOfGrades
        fields = ['grade', 'parallel']


class AdministratorTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorTypes
        fields = ['choosing']


class NamesOfOlympiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamesOfOlympia
        fields = ['choosing']
