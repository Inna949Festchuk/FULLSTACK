from rest_framework import serializers
from .models import PointInLine, WorldPoint, WorldLine


# сериализатор данных, поступивших в POST-запросе создания ориентиров
class WorldPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldPoint
        fields = ['name', 'location',] 


# сериализатор данных, поступивших в POST-запросе запуска геосервиса
class WorldLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldLine
        fields = ['name', 'azimuth', 'pn', 'distance',] 


# сериализатор записи постобработанных геосервисом данных в БД
class WorldLineSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = WorldLine
        fields = ['name', 'azimuth', 'pn', 'distance', 'location',] 
        
        
# сериализатор записи связей M:N в БД
class PointInLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointInLine
        fields = ['mypoints', 'mylines',] 





    #     # Это GeoJSON - результат сериализации (ЭТО СТРОКА не словарь!!!)
        # {"type": "FeatureCollection", 
        # "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}, 
        # "features": [
        #     {"type": "Feature", 
        #     "properties": 
        #     {"name": "точка созданная в QGIS", 
        #     "x": " - ", 
        #     "y": " - "}, 
        #     "geometry": {"type": "Point", "coordinates": [954158.0690369561, 4215137.097267967]}}, 
            
        #     {"type": "Feature", 
        #     "properties": {"name": "вторая точка созданная в QGIS", 
        #     "x": " - ", 
        #     "y": " - "}, 
        #     "geometry": {"type": "Point", "coordinates": [954158.1078318285, 4215137.122402673]}}, 

        #     {"type": "Feature", 
        #     "properties": {"name": "третья точка", 
        #     "x": " - ", 
        #     "y": " - "}, 
        #     "geometry": {"type": "Point", "coordinates": [954158.1330119616, 4215137.0986461975]}}, 

        #     {"type": "Feature", 
        #     "properties": {"name": "далеко", 
        #     "x": " - ", 
        #     "y": " - "}, 
        #     "geometry": {"type": "Point", "coordinates": [954187.8349256464, 4215153.366149437]}}]}