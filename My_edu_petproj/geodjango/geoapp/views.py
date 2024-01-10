from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import WorldPoint, WorldLine, PointInLine
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry, LineString
from .serializers import PointInLineSerializer, WorldLineSerializer, WorldLineSerializerPost, WorldPointSerializer
from django.core.serializers import serialize, deserialize
import json
import math
import copy

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

@api_view(['POST'])
def create_point(request):
    '''
    ПОДКЛЮЧИ ЭТО К КНОПКЕ
    PATH {{baseUrl}}/api/create_point/
    {"name": #1,
    "location": "SRID=4326;POINT(954158.1 4215137.1)"
    }
    import requests
    url = "http://127.0.0.1:8000/api/create_point/"
    response = requests.post(url, data={"name": #1, "location": "SRID=4326;POINT(954158.1 4215137.1)"})
    response.json()
    '''
    # Отправляем байтстринг сериализатору
    serialpoint = WorldPointSerializer(data=request.data)
    # проверяем десериализованные данные на валидность
    if serialpoint.is_valid():
        # если данные валидны, сохраняем их в БД
        serialpoint.save()
        return Response(serialpoint.data)
    else:
        print('ERROR! No valid data!')
        return Response(serialpoint.errors)

# сервис построения схемы движения по азимутам 
# Декоратор для преобразования простого обработчика в API-бработчик
@api_view(['POST'])
def create_line(request):
    '''
    Создание точки
    PATCH {{baseUrl}}/create_line/
    {"pn": 5.5}
    import requests
    url = "http://127.0.0.1:8000/api/create_line/"
    response = requests.post(url, data={"pn": 5.5})
    response.content
    '''

    # расчет азимута и расстояния в пар-шагах
    def Am(x1, y1, x2, y2, Pn=0):
        '''
        Функция расчета азимута магнитного с учетом поправки направления
        и расстояния между ориентирами в пар-шагах
        Pn - поправка направления (по-умолчанию 0 град)
        '''
        # Расчитываем расстояние между точками в п.ш.
        dX = x2 - x1
        dY = y2 - y1
        if dX == 0:
            r = 90
        elif dY == 0:
            r = 0
        else:
            r = (180 / math.pi) * math.atan(math.fabs(dY / dX))
        
        S = math.sqrt(dX ** 2 + dY ** 2) / 1.5
        
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
        Am_min = int(60 * (Am_degre - Am_grad))
        Am_sec = round(60 * (60 * (Am_degre - int(Am_degre)) - Am_min), 1)
        # Объединяем все в одну строку
        Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
        # Округляем п.ш.
        S = f'{S:.1f} п.ш.'
        return Am, S
    
    # извлечение координат точек из БД
    
    points = [point.location.coords for point in WorldPoint.objects.all()]
    
    # извлечение значения поправки направления из тела запроса (десериализация request.data)
    serialline = WorldLineSerializer(data=request.data)
    # print(serialline)
    # проверка поступивших (влияние помех в канале передачи данных)
    # данных на валидность
    if serialline.is_valid():
        # если данных нет принять по-умолчанию ПН=0
        pn = serialline.data.get('pn', 0)

        for cnt in range(len(points) - 1):
            # рассчет азимута и расстояния в пар-шагах
            # res = Am(points[cnt][0], points[cnt][1], points[cnt + 1][0], points[cnt + 1][1], Pn=float(pn))
            # меняем порядок координат XY на YX для SRID = 28404
            res = Am(points[cnt][1], points[cnt][0], points[cnt + 1][1], points[cnt + 1][0], Pn=float(pn))

            # создание линий на основе извлекаемых точек
            # СК-42, 6-градусная зона №4 (SRID = 28404 = порядок YX)
            new_line = LineString(points[cnt], points[cnt + 1], srid=28404)
            # new_line.transform(28404) # Изменение локации согласно SRID

            myname = f'Ориентир: {cnt + 1} - ориентир: {cnt + 2}'
            # создаем структуру данных (словарь) для сериализации - 
            # преобразования в байт-поток перед записью в БД
            dictpost = dict(name=myname, azimuth=res[0], pn=float(pn), distance=res[1], location=new_line)
            # сериализуем (параметру запроса data присваеваем словарь dictpost, передаваемый в теле запроса)
            seriallinepost = WorldLineSerializerPost(data=dictpost)
            # если сериализованные данные валидны записать их в БД
            if seriallinepost.is_valid():
                seriallinepost.save()
                # это вариант, если БД и сервис находятся на одном сервере
                # WorldLine(azimuth=res[0], pn=float(pn), distance=res[1], location=new_line).save()
            else:
                print('ERROR! No valid data POST!')
                return Response(seriallinepost.errors)

        # Заполняем таблицу связей
        # Получаем id экземпляров модели WorldLine
        idlins = [lin.id for lin in WorldLine.objects.all()]
        
        listpointinline = []

        for idlin in idlins:
            # проходим по каждой линии в соответствии с ее id
            line = WorldLine.objects.get(id=idlin)
            # и ищем точки с которыми она пересекается location__intersects
            # где location - поле с геометрией __intersects - метод поиска пересечений
            pnts_intersect = WorldPoint.objects.filter(location__intersects=line.location)
            
            # формируем список со вложенными словарями пересечений
            # это нужно чтобы сформировать связи между конкретной линией и 
            # точками с которыми она пересекается
            for pnt_intersect in pnts_intersect:
                data = {'mypoints': pnt_intersect.id, 'mylines': line.id}
                listpointinline.append(data)
        
        # сохраняем все записи одновременно после цикла
        # формируя таблицу N:M
        serialpointinline = PointInLineSerializer(data=listpointinline, many=True)
        if serialpointinline.is_valid():
            serialpointinline.save()
        else:
            print('ERROR! No valid data N:M!')
            return Response(serialpointinline.errors)
            
        # формирование GeoJSON для визуализации в браузере с помощью Leaflet
        # сериализация (представляет собой процесс преобразования состояния объекта в форму, пригодную для сохранения или передачи)
        # Объекты модели, для сохранения или передачи, нужно СЕРИАЛИЗОВЫВАТЬ - преобразовывать в байт-код (поток)
        # data_geojson_str_pnt = serialize('geojson', WorldPoint.objects.all(),
        #         geometry_field='location',
        #         fields=('name', 'location',))
        # data_geojson_str_line = serialize('geojson', WorldLine.objects.all(),
        #         geometry_field='location',
        #         fields=('azimuth', 'pn', 'distance', 'location',))
        # десериализация (преобразование серриализованныех данныех (потока) обратно в структуру словаря (str->dict))
        # context_pnt = json.loads(data_geojson_str_pnt)
        # context_line = json.loads(data_geojson_str_line)
        
        # возврат GeoJSON (введи response.content )
        # return Response({'content': (context_pnt, context_line)})
        
        return Response(serialline.data)
    else:
        Response(serialline.errors)

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


    

