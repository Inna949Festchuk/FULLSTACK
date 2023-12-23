from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import WorldPoint, WorldLine
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry, LineString
from .serializers import WorldLineSerializer, WorldPointSerializer
from django.core.serializers import serialize, deserialize
import json
import math
import copy
from django.contrib.gis.db.models.functions import IsValid

# получение point
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

# сервис построения схемы движения по азимутам 
# Декоратор для преобразования простого обработчика в API-бработчик
@api_view(['POST'])
def create_line(request):
    '''
    Создание точки
    PATCH {{baseUrl}}/create_line/
    {'pn': 5.5}
    import requests
    url = "http://127.0.0.1:8000/api/create_line/"
    response = requests.post(url, data={'pn': 5.5})
    response.content
    '''

    # расчет азимута и расстояния в пар-шагах
    def Am(x1, y1, x2, y2, Pn=0):
        '''
        Pn - поправка направления (по-умолчанию 1 град)
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
    
    # извлечение координат точек из БД
    
    # # сериализация
    # serpoint = WorldPointSerializer(WorldPoint.objects.all(), many=True)
    # # many=True означает что серриалайзер выдаст нам все объекты
    # datapoint = serpoint.data # десериализация
    # print(datapoint)
    # # [OrderedDict([('name', 'вторая точка'), ('location', 'SRID=4326;POINT (9469366.619189991 10373434.66280238)')]), 
    # # OrderedDict([('name', 'третья точка'), ('location', 'SRID=4326;POINT (40044173.59302919 34136100.13507251)')]), 
    # # OrderedDict([('name', 'четвертая точка'), ('location', 'SRID=4326;POINT (5025508.686525814 33178142.73641437)')])]
    # # Попробывать так 
    # points = [point.location.coords for point in datapoint или serpoint]
    # # Вместо этого
    points = [point.location.coords for point in WorldPoint.objects.all()]
    # извлечение значения поправки направления из тела запроса
    # если данных нет принять по-умолчанию ПН=1
    pn = request.data.get('pn', 0)

    for cnt in range(len(points) - 1):
        # рассчет азимута и расстояния в пар-шагах
        res = Am(points[cnt][0], points[cnt][1], points[cnt + 1][0], points[cnt + 1][1], Pn=float(pn))
        
        # создание линий на основе извлекаемых точек
        new_line = LineString(points[cnt], points[cnt + 1], srid=4326)
        
        
        # new_line = LineString([point for point in points])
        
        # serline = WorldLineSerializer(WorldLine.objects.all(), many=True)
        # dataline = serserline.data 

        # Если геометрия правильно сформирована (валидна) то записать в БД и сформировать geojson
        # if IsValid(new_line) == True:
            # запись в БД расчетных значений
            # serline(azimuth=res[0], pn=float(pn), distance=res[1], location=new_line).save()
            # WorldLine(azimuth=res[0], pn=float(pn), distance=res[1], location=new_line).save()
            # print(float(request.data.get('pn', 1)))  
            
        WorldLine(azimuth=res[0], pn=float(pn), distance=res[1], location=new_line).save()
        # else:
        #     print('НЕВАЛИДНЫЕ ДАННЫЕ!')
    
    # pnts = [pnt.id for pnt in WorldPoint.objects.all()]
    # lins = [lin.id for lin in WorldLine.objects.all()]
    # # pnts_copy = copy.copy(tuple(pnts))
    # # lins_copy = copy.copy(tuple(lins))
    # pnts_copy = copy.copy(tuple(pnts))
    # lins_copy = copy.copy(tuple(lins))
    # print(pnts_copy, lins_copy)
    # book.authors.add(author1, author2)
    
    # idpoints = [idpoint.id for idpoint in WorldPoint.objects.all()]
    # idlines = [idline.id for idline in WorldLine.objects.all()]
    
    # for cnt in range(1, len(idpoints) - 2):
    #     PointInLine(mypoints=WorldPoint.objects.get(id=cnt + 1), mylines=WorldLine.objects.get(id=cnt)).save()
    #     PointInLine(mypoints=WorldPoint.objects.get(id=cnt + 1), mylines=WorldLine.objects.get(id=cnt)).save()
    
    
    # for i in range(1, len(idpoints)):
    #     world_point_instance = WorldPoint.objects.get(id=i)  # Получаем экземпляр WorldPoint
    #     world_line_instance = WorldLine.objects.get(id=i)
    #     posit_in_line_instance = PositInLine(mypoints=world_point_instance, mylines=world_line_instance)  # Присваиваем этот экземпляр атрибуту mypoints
    #     posit_in_line_instance = PositInLine(mypoints=world_point_instance, mylines=world_line_instance)
    #     # posit_in_line_instance.save()  # Сохраняем экземпляр PositInLine
    #     print(world_point_instance)

   
    # формирование GeoJSON для визуализации в браузере с помощью Leaflet
    # сериализация (представляет собой процесс преобразования состояния объекта в форму, пригодную для сохранения или передачи)
    # Объекты модели, для сохранения или передачи, нужно СЕРИАЛИЗОВЫВАТЬ - преобразовывать в байт-код (поток)
    data_geojson_str_pnt = serialize('geojson', WorldPoint.objects.all(),
            geometry_field='location',
            fields=('name', 'location',))
    data_geojson_str_line = serialize('geojson', WorldLine.objects.all(),
            geometry_field='location',
            fields=('azimuth', 'pn', 'distance', 'location',))
    # десериализация (преобразование серриализованныех данныех (потока) обратно в структуру словаря (str->dict))
    context_pnt = json.loads(data_geojson_str_pnt)
    context_line = json.loads(data_geojson_str_line)
    
    # возврат GeoJSON (введи response.content )
    return Response({'content': (context_pnt, context_line)})


# # - - - - - - - - - - -
# # ВТОРОЙ ВАРИАНТ
# # - - - - - - - - - - -

# # ДЖЕНЕРИКИ
# from rest_framework.generics import ( 
#     ListAPIView, 
# )
# # МИКСИНЫ
# from rest_framework.mixins import ( 
#     CreateModelMixin,
#     UpdateModelMixin, 
# )


# class PointAPIView(ListAPIView, CreateModelMixin, UpdateModelMixin):
#     # Получение сериализованного списка точек GET {{baseUrl}}/point/
#     queryset = WorldPoint.objects.all()
#     serializer_class = WorldPointSerializer
    # def uppdate_bgd(self, **kwargs):
    #     data = super().uppdate_bgd(**kwargs)
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
    #     id_points = [point.id for point in WorldPoint.objects.all()]
    #     # print(points)
    #     # print(id_points)
            
                
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
    #     for cnt, id_point in zip(data["features"], id_points):
    #         cnt["properties"]["x"] = result_azimuth[i]
    #         field_azimuth = cnt["properties"]["x"]
    #         cnt["properties"]["y"] = result_distance_ph[i]
    #         field_distance_ph = cnt["properties"]["y"]
    #         i += 1
    #         # Фильтруем экземпляры модели по id и обновляем в них расчетные значения 
    #         WorldPoint.objects.filter(id=id_point).update(**cnt["properties"])
    #         # print(field_azimuth, field_distance_ph)
    #         # print(id_point)
    #     # Вызываем функцию обновления Базы данных
    #     return data



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


    

