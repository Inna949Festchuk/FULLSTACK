from rest_framework import serializers
from django.core.serializers import serialize, deserialize
# from .models import WorldLine
from .models import WorldPoint
import json
import math 

# from django.contrib.gis.db.models.functions import AsWKT, Azimuth
# from django.contrib.gis.geos import Point, LineString
# from math import degrees

# опишите необходимые сериализаторы

class WorldPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldPoint
        fields = ['name', 'x', 'y', 'location',] 

        # Считаем азимут
        # point1 = WorldPoint.objects.get(id=16).location
        # point2 = WorldPoint.objects.get(id=17).location
        # point1 = Point(10, 50, srid=4326)
        # point2 = Point(40, 60, srid=4326)
        # ls1 = LineString(point1, point2)
        # azimuth_rad = Azimuth(point1, point2)
        # azimuth_deg = degrees(azimuth_rad) if azimuth_rad is not None else None
        # print(ls1.coords[0])
        # Библиотека GEOS. GEOSGeometry.distance(geom) Возвращает расстояние между ближайшими точками данной геометрии и заданной geom (другой объект GEOSGeometry).
        # dist = point1.distance(point2)
        # print(dist)
        # print(point1.x)
          
        # def Am(x1, y1, x2, y2, Pn=1):
        #     '''
        #     Pn - поправка направления
        #     '''
        #     # Расчитываем расстояние между точками в п.ш.
        #     dX = x2 - x1
        #     dY = y2 - y1
        #     if dX == 0:
        #         r = 90
        #     elif dY == 0:
        #         r = 0
        #     else:
        #         r = (180/math.pi)*math.atan(math.sqrt((dY/dX)**2))
            
        #     S = math.sqrt(dX**2 + dY**2)/1.5
            
        #     # Расчитываем азумут магнитный с учетом поправки направления
        #     if dX >= 0 and dY >= 0:
        #         a = r
        #     elif dX < 0 and dY > 0:
        #         a = 180 - r
        #     elif dX <= 0 and dY <= 0:
        #         a = 180 + r
        #     else:
        #         a = 360 - r
            
        #     # Учитываем поправку направления
        #     Am_degre = a - Pn
        #     # Пересчитываем десятичные градусы в градусы, минуты, секунды
        #     Am_grad = int(Am_degre)
        #     Am_min = int(60*(Am_degre - Am_grad))
        #     Am_sec = round(60*(60*(Am_degre - int(Am_degre)) - Am_min), 1)
        #     # Объединяем все в одну строку
        #     Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
        #     # Округляем п.ш.
        #     S = f'{S:.0f} п.ш.'
        #     return Am, S

        # # Извлекаем в список значения пар координат из модели WorldPoint
        # points = WorldPoint.objects.all()
        # points = [point.location.coords for point in points]
        # # print(points)
        
        # # - - - - - - - - - - 
        # # ЗДЕСЬ НУЖНО СОЗДАТЬ ЛИНИИ ИЗ points И ДОБАВИТЬ ИХ В models.py создав новую модель LINEARSTRING
        # # - - - - - - - - - - 
    
        # # Формируем два словаря и помещаем в них результаты расчетов азимута и расстояния в п.ш.
        # result_azimuth = ['Старт']
        # result_distance_ph = ['Старт']
        # for cnt in range(len(points)-1):
        #     res = Am(points[cnt][0], points[cnt][1], points[cnt+1][0], points[cnt+1][1])
        #     result_azimuth.append(res[0])
        #     result_distance_ph.append(res[1])
        # # print(result_azimuth, result_distance_ph)

        # # Активируй если надо посмотреть результат сериализации
        # data_geojson_str = serialize('geojson', WorldPoint.objects.all(),
        #     geometry_field='location',
        #     fields=('name', 'x', 'y', 'location',))
        # # формируем словарь из строки datastr
        # data = json.loads(data_geojson_str)

        # # перезаписываем результаты расчета в словарь в поля x - азимут и y - растояние в п.ш.  
        # i = 0
        # for cnt in data["features"]:
        #     cnt["properties"]["x"] = result_azimuth[i]
        #     field_azimuth = cnt["properties"]["x"]
        #     cnt["properties"]["y"] = result_distance_ph[i]
        #     field_distance_ph = cnt["properties"]["y"]
        #     i += 1
        #     # print(field_azimuth, field_distance_ph)
        # print(data)

        # def Am(x1, y1, x2, y2, Pn=1):
        #     '''
        #     Pn - поправка направления
        #     '''
        #     # Расчитываем расстояние между точками в п.ш.
        #     dX = x2 - x1
        #     dY = y2 - y1
        #     if dX == 0:
        #         r = 90
        #     elif dY == 0:
        #         r = 0
        #     else:
        #         r = (180/math.pi)*math.atan(math.sqrt((dY/dX)**2))
                
        #     S = math.sqrt(dX**2 + dY**2)/1.5
                
        #     # Расчитываем азумут магнитный с учетом поправки направления
        #     if dX >= 0 and dY >= 0:
        #         a = r
        #     elif dX < 0 and dY > 0:
        #         a = 180 - r
        #     elif dX <= 0 and dY <= 0:
        #         a = 180 + r
        #     else:
        #         a = 360 - r
                
        #     # Учитываем поправку направления
        #     Am_degre = a - Pn
        #     # Пересчитываем десятичные градусы в градусы, минуты, секунды
        #     Am_grad = int(Am_degre)
        #     Am_min = int(60*(Am_degre - Am_grad))
        #     Am_sec = round(60*(60*(Am_degre - int(Am_degre)) - Am_min), 1)
        #     # Объединяем все в одну строку
        #     Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
        #     # Округляем п.ш.
        #     S = f'{S:.0f} п.ш.'
        #     return Am, S

        # # Извлекаем в список значения пар координат из модели WorldPoint
        # points = WorldPoint.objects.all()
        # points = [point.location.coords for point in points]
        # id_points = [point.id for point in WorldPoint.objects.all()]
        # # print(points)
        # # print(id_points)
        
            
        # # - - - - - - - - - - 
        # # ЗДЕСЬ НУЖНО СОЗДАТЬ ЛИНИИ ИЗ points И ДОБАВИТЬ ИХ В models.py создав новую модель LINEARSTRING
        # # - - - - - - - - - - 
        
        # # Формируем два словаря и помещаем в них результаты расчетов азимута и расстояния в п.ш.
        # result_azimuth = ['Старт']
        # result_distance_ph = ['Старт']
        # for cnt in range(len(points)-1):
        #     res = Am(points[cnt][0], points[cnt][1], points[cnt+1][0], points[cnt+1][1])
        #     result_azimuth.append(res[0])
        #     result_distance_ph.append(res[1])
        # # print(result_azimuth, result_distance_ph)

        # # GeoDjango предоставляет специальный сериализатор для формата GeoJSON.
        # # Все записи из БД преобразуются в GeoJSON
        # data_geojson_str = serialize('geojson', WorldPoint.objects.all(),
        #     geometry_field='location',
        #     fields=('name', 'x', 'y', 'location',))
        # # формируем словарь из строки datastr
        # data = json.loads(data_geojson_str)

        # # перезаписываем результаты расчета в словарь в поля x - азимут и y - растояние в п.ш.  
        # i = 0
        # for cnt, id_point in zip(data["features"], id_points):
        #     cnt["properties"]["x"] = result_azimuth[i]
        #     field_azimuth = cnt["properties"]["x"]
        #     cnt["properties"]["y"] = result_distance_ph[i]
        #     field_distance_ph = cnt["properties"]["y"]
        #     i += 1
        #     # Фильтруем экземпляры модели по id и обновляем в них расчетные значения 
        #     WorldPoint.objects.filter(id=id_point).update(**cnt["properties"])
        #     # print(field_azimuth, field_distance_ph)
        #     print(id_point)

        # id_points = [point.id for point in WorldPoint.objects.all()]
        # Создание записи в БД на основе расчета
            
        # WorldPoint.objects.update(**cnt["properties"])
        
        # Это GeoJSON - результат сериализации (ЭТО СТРОКА не словарь!!!)
        {"type": "FeatureCollection", 
        "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}, 
        "features": [
            {"type": "Feature", 
            "properties": 
            {"name": "точка созданная в QGIS", 
            "x": " - ", 
            "y": " - "}, 
            "geometry": {"type": "Point", "coordinates": [954158.0690369561, 4215137.097267967]}}, 
            
            {"type": "Feature", 
            "properties": {"name": "вторая точка созданная в QGIS", 
            "x": " - ", 
            "y": " - "}, 
            "geometry": {"type": "Point", "coordinates": [954158.1078318285, 4215137.122402673]}}, 

            {"type": "Feature", 
            "properties": {"name": "третья точка", 
            "x": " - ", 
            "y": " - "}, 
            "geometry": {"type": "Point", "coordinates": [954158.1330119616, 4215137.0986461975]}}, 

            {"type": "Feature", 
            "properties": {"name": "далеко", 
            "x": " - ", 
            "y": " - "}, 
            "geometry": {"type": "Point", "coordinates": [954187.8349256464, 4215153.366149437]}}]}