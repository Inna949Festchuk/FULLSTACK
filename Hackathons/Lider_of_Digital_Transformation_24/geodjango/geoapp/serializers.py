from rest_framework import serializers
from .models import PointInLine, ImportTrek, ImportTrekLine, ImportInc, Person


class ImportTrekSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTrek
        fields = ['name', 'location',] 


class ImportTrekLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTrekLine
        fields = ['name', 'azimuth', 'pn', 'distance',] 


class ImportTrekLineSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ImportTrekLine
        fields = ['name', 'azimuth', 'pn', 'distance', 'location',] 


class PointInLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointInLine
        fields = ['mypoints', 'mylines',] 


class ImportIncSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImportInc
        fields = ['name', 'location',] 
        

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['person_name',] 
