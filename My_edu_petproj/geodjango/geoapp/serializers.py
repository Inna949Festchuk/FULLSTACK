from rest_framework import serializers
from django.core.serializers import serialize, deserialize
# from .models import WorldLine
from .models import WorldPoint, WorldLine
import json
import math 

# from django.contrib.gis.db.models.functions import AsWKT, Azimuth
# from django.contrib.gis.geos import Point, LineString
# from math import degrees

# опишите необходимые сериализаторы

class WorldPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldPoint
        fields = ['name', 'location',] 

class WorldLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldLine
        fields = ['azimuth', 'pn', 'distance', 'location',] 

                
    #     # Это GeoJSON - результат сериализации (ЭТО СТРОКА не словарь!!!)
    #     {"type": "FeatureCollection", 
    #     "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}, 
    #     "features": [
    #         {"type": "Feature", 
    #         "properties": 
    #         {"name": "точка созданная в QGIS", 
    #         "x": " - ", 
    #         "y": " - "}, 
    #         "geometry": {"type": "Point", "coordinates": [954158.0690369561, 4215137.097267967]}}, 
            
    #         {"type": "Feature", 
    #         "properties": {"name": "вторая точка созданная в QGIS", 
    #         "x": " - ", 
    #         "y": " - "}, 
    #         "geometry": {"type": "Point", "coordinates": [954158.1078318285, 4215137.122402673]}}, 

    #         {"type": "Feature", 
    #         "properties": {"name": "третья точка", 
    #         "x": " - ", 
    #         "y": " - "}, 
    #         "geometry": {"type": "Point", "coordinates": [954158.1330119616, 4215137.0986461975]}}, 

    #         {"type": "Feature", 
    #         "properties": {"name": "далеко", 
    #         "x": " - ", 
    #         "y": " - "}, 
    #         "geometry": {"type": "Point", "coordinates": [954187.8349256464, 4215153.366149437]}}]}