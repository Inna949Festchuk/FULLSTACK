from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import WorldPoint
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from .serializers import WorldPointSerializer
from django.core.serializers import serialize, deserialize
import json
import math

# # получение point
# @api_view(['GET'])
# def show_point(request):
#     point = WorldPoint.objects.all()
#     data = WorldPointSerializer(point, many=True)
#     return Response(data.data)

# # создание point
# @api_view(['POST'])
# def create_point(request):
#     name = request.GET.get('name', 'No name')
#     x = request.GET.get('x')
#     y = request.GET.get('y')
#     pnt = GEOSGeometry(f'SRID=32140;POINT({float(x)} {float(y)})')
#     WorldPoint(name=name, x=float(x), y=float(y), location=pnt).save()
#     return Response({'status': 'point create'})

# # - - - - - - - - - - -
# # ВТОРОЙ ВАРИАНТ
# # - - - - - - - - - - -

# ДЖЕНЕРИКИ
from rest_framework.generics import ( 
    ListAPIView, 
)
# МИКСИНЫ
from rest_framework.mixins import ( 
    CreateModelMixin,
    UpdateModelMixin, 
)


class PointAPIView(ListAPIView, CreateModelMixin, UpdateModelMixin):
    # Получение сериализованного списка точек GET {{baseUrl}}/point/
    queryset = WorldPoint.objects.all()
    serializer_class = WorldPointSerializer

    def Am(x1, y1, x2, y2, Pn=1):
        '''
        Pn - поправка направления
        '''
        # Расчитываем расстояние между точками в п.ш.
        dX = x2 - x1
        dY = y2 - y1
        if dX == 0:
            r = 90
        elif dY == 0:
            r = 0
        else:
            r = (180/math.pi)*math.atan(math.sqrt((dY/dX)**2))
                
        S = math.sqrt(dX**2 + dY**2)/1.5
                
        # Расчитываем азумут магнитный с учетом поправки направления
        if dX >= 0 and dY >= 0:
            a = r
        elif dX < 0 and dY > 0:
            a = 180 - r
        elif dX <= 0 and dY <= 0:
            a = 180 + r
        else:
            a = 360 - r
                
        # Учитываем поправку направления
        Am_degre = a - Pn
        # Пересчитываем десятичные градусы в градусы, минуты, секунды
        Am_grad = int(Am_degre)
        Am_min = int(60*(Am_degre - Am_grad))
        Am_sec = round(60*(60*(Am_degre - int(Am_degre)) - Am_min), 1)
        # Объединяем все в одну строку
        Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
        # Округляем п.ш.
        S = f'{S:.0f} п.ш.'
        return Am, S

    # Извлекаем в список значения пар координат из модели WorldPoint
    points = WorldPoint.objects.all()
    points = [point.location.coords for point in points]
    id_points = [point.id for point in WorldPoint.objects.all()]
    # print(points)
    # print(id_points)
        
            
    # - - - - - - - - - - 
    # ЗДЕСЬ НУЖНО СОЗДАТЬ ЛИНИИ ИЗ points И ДОБАВИТЬ ИХ В models.py создав новую модель LINEARSTRING
    # - - - - - - - - - - 
        
    # Формируем два словаря и помещаем в них результаты расчетов азимута и расстояния в п.ш.
    result_azimuth = ['Старт']
    result_distance_ph = ['Старт']
    for cnt in range(len(points)-1):
        res = Am(points[cnt][0], points[cnt][1], points[cnt+1][0], points[cnt+1][1])
        result_azimuth.append(res[0])
        result_distance_ph.append(res[1])
    # print(result_azimuth, result_distance_ph)

    # GeoDjango предоставляет специальный сериализатор для формата GeoJSON.
    # Все записи из БД преобразуются в GeoJSON
    data_geojson_str = serialize('geojson', WorldPoint.objects.all(),
        geometry_field='location',
        fields=('name', 'x', 'y', 'location',))
    # формируем словарь из строки datastr
    data = json.loads(data_geojson_str)

    # перезаписываем результаты расчета в словарь в поля x - азимут и y - растояние в п.ш.  
    i = 0
    for cnt, id_point in zip(data["features"], id_points):
        cnt["properties"]["x"] = result_azimuth[i]
        field_azimuth = cnt["properties"]["x"]
        cnt["properties"]["y"] = result_distance_ph[i]
        field_distance_ph = cnt["properties"]["y"]
        i += 1
        # Фильтруем экземпляры модели по id и обновляем в них расчетные значения 
        WorldPoint.objects.filter(id=id_point).update(**cnt["properties"])
        # print(field_azimuth, field_distance_ph)
        print(id_point)



    # def post(self, request, *args, **kwargs):
    #     '''
    #     Создание точки
    #     PATCH {{baseUrl}}/point/
    #     '''
    #     return self.create(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     '''
    #     Обновление точки
    #     PATCH {{baseUrl}}/point/{{id}}/
    #     '''
          
    #     # Создаем функцию для расчета азимута магнитного с учетом поправки направления 
    #     # и расстояния в п.ш.
        
    #     def Am(x1, y1, x2, y2, Pn=1):
    #         '''
    #         Pn - поправка направления
    #         '''
    #         # Расчитываем расстояние между точками в п.ш.
    #         dX = x2 - x1
    #         dY = y2 - y1
    #         if dX == 0:
    #             r = 90
    #         elif dY == 0:
    #             r = 0
    #         else:
    #             r = (180/math.pi)*math.atan(math.sqrt((dY/dX)**2))
            
    #         S = math.sqrt(dX**2 + dY**2)/1.5
            
    #         # Расчитываем азумут магнитный с учетом поправки направления
    #         if dX >= 0 and dY >= 0:
    #             a = r
    #         elif dX < 0 and dY > 0:
    #             a = 180 - r
    #         elif dX <= 0 and dY <= 0:
    #             a = 180 + r
    #         else:
    #             a = 360 - r
            
    #         # Учитываем поправку направления
    #         Am_degre = a - Pn
    #         # Пересчитываем десятичные градусы в градусы, минуты, секунды
    #         Am_grad = int(Am_degre)
    #         Am_min = int(60*(Am_degre - Am_grad))
    #         Am_sec = round(60*(60*(Am_degre - int(Am_degre)) - Am_min), 1)
    #         # Объединяем все в одну строку
    #         Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
    #         # Округляем п.ш.
    #         S = f'{S:.0f} п.ш.'
    #         return Am, S

    #     # Извлекаем в список значения пар координат из модели WorldPoint
    #     points = WorldPoint.objects.all()
    #     points = [point.location.coords for point in points]
    #     # print(points)
        
    #     # - - - - - - - - - - 
    #     # ЗДЕСЬ НУЖНО СОЗДАТЬ ЛИНИИ ИЗ points И ДОБАВИТЬ ИХ В models.py создав новую модель LINEARSTRING
    #     # - - - - - - - - - - 
    
    #     # Формируем два словаря и помещаем в них результаты расчетов азимута и расстояния в п.ш.
    #     result_azimuth = ['Старт']
    #     result_distance_ph = ['Старт']
    #     for cnt in range(len(points)-1):
    #         res = Am(points[cnt][0], points[cnt][1], points[cnt+1][0], points[cnt+1][1])
    #         result_azimuth.append(res[0])
    #         result_distance_ph.append(res[1])
    #     # print(result_azimuth, result_distance_ph)

    #     # GeoDjango предоставляет специальный сериализатор для формата GeoJSON.
    #     # Все записи из БД преобразуются в GeoJSON
    #     data_geojson_str = serialize('geojson', WorldPoint.objects.all(),
    #         geometry_field='location',
    #         fields=('name', 'x', 'y', 'location',))
    #     # формируем словарь из строки datastr
    #     data = json.loads(data_geojson_str)

    #     # перезаписываем результаты расчета в словарь в поля x - азимут и y - растояние в п.ш.  
    #     i = 0
    #     for cnt in data["features"]:
    #         cnt["properties"]["x"] = result_azimuth[i]
    #         field_azimuth = cnt["properties"]["x"]
    #         cnt["properties"]["y"] = result_distance_ph[i]
    #         field_distance_ph = cnt["properties"]["y"]
    #         i += 1
    #         # print(field_azimuth, field_distance_ph)
    #         print(cnt["properties"])
            
    #         # for deserialized_object in deserialize("json", data_geojson_str):
    #         #     if object_should_be_saved(deserialized_object):
    #         #         deserialized_object.save()

    #         # Создание записи в БД на основе расчета
    #         return self.partial_update(request, cnt["properties"])


    

