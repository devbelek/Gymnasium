from rest_framework import serializers
from .models import NameOfGrades, AdministratorTypes, NamesOfOlympia, Contacts


class NameOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameOfGrades
        exclude = ['id']


class AdministratorTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorTypes
        exclude = ['id']


class NamesOfOlympiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamesOfOlympia
        exclude = ['id']


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        exclude = ['id']
