from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import WorldPoint, WorldLine, PointInLine
from rest_framework.response import Response
from rest_framework import status # Отображаем ошибки 404 на странице
from django.contrib.gis.geos import GEOSGeometry, LineString
from .serializers import PointInLineSerializer, WorldLineSerializer, WorldLineSerializerPost, WorldPointSerializer
from django.core.serializers import serialize, deserialize
from django.contrib.gis.geos import GEOSGeometry
# Обеспечиваем атамарность при работе с данными БД (читай ниже)
from django.db import transaction
# - - - - - - - - - - - - - - -
# Импорт шаблонизатора
from django.views.generic import TemplateView
# - - - - - - - - - - - - - - -

import json
import math
import copy

# получение point
@api_view(['GET'])
def show_point(request):
    # Создаем объекты модели WorldPoint
    point = WorldPoint.objects.all()
    # Сериализуем извлеченные объекты БД:
    # - - - - - - - - - - - - - - - - - - - - -
    # Создаем объект класса сериализатора
    data = WorldPointSerializer(point, many=True) # many=True - сериализуем все записи point
    
    print(data, type(data)) # Объект класса сериализатора:
    # WorldPointSerializer(<QuerySet [<WorldPoint: Ориентир: 1>]>, <WorldPoint: Ориентир: 120>, many=True):
    # name = CharField(help_text='Введите название ориентира', label='Название ориентира', max_length=250) 
    # location = ModelField(label='Схема ориентиров', model_field=<django.contrib.gis.db.models.fields.PointField: location>)

    print(data.data, type(data.data)) # Извлекаем из объекта класса сериализатора данные в виде списка словарей OrderedDict:
    # [OrderedDict([('name', '1'), ('location', 'SRID=28404;POINT (4483847.704276834 6060087.566537171)')]), 
    # OrderedDict([('name', '120'), ('location', 'SRID=28404;POINT (4499753.881367749 6059924.900537257)')])]

    # return Response(data.data) # Response (аналог JSONRenderer().render(data.data)) 
                               # сериализует список словарей в JSON, преобразованный в байтовую строку b' И ПЕРЕДАЕТ КЛИЕНТУ (см. ниже ТОЖЕ САМОЕ)
    # ТОЖЕ САМОЕ
    from rest_framework.renderers import JSONRenderer
    print(JSONRenderer().render(data.data)) # сериализует список словарей в JSON, преобразованный в байтовую строку b' 
    # И ПЕРЕДАЕТ КЛИЕНТУ !!! (так работает функция encoder()) !!!
    # b'[{"name":"1","location":"SRID=28404;POINT (4483847.704276834 6060087.566537171)"},
    # {"name":"120","location":"SRID=28404;POINT (4499753.881367749 6059924.900537257)"}]
    return Response(JSONRenderer().render(data.data))

# получение line
@api_view(['GET'])
def show_line(request):
    line = WorldLine.objects.all()
    data = WorldLineSerializerPost(line, many=True)
    return Response(data.data)

# # создание point
# @api_view(['POST'])
# def create_point(request):
#     name = request.GET.get('name', 'No name')
#     x = request.GET.get('x')
#     y = request.GET.get('y')
#     pnt = GEOSGeometry(f'SRID=32140;POINT({float(x)} {float(y)})')
#     WorldPoint(name=name, x=float(x), y=float(y), location=pnt).save()
#     return Response({'status': 'point create'})

# сервис добавления ориентиров в базу данных    
@api_view(['POST'])
def create_point(request): 
    '''
    ПОДКЛЮЧИ ЭТО К КНОПКЕ
    PATH {{baseUrl}}/api/create_point/
    {
    "name": "WGS84", 
    "location": "SRID=4326;POINT(21.7 54.5)"
    }
    {
    "name": "Pulkovo42", 
    "location": "SRID=28404;POINT(4475167 6061130)"
    }
    import requests
    url = "http://127.0.0.1:8000/api/create_point/"
    response = requests.post(url, data={"name": "test", "location": "SRID=28404;POINT(4475177 6061145)"})
    response.json()
    '''
    # Код ниже относится к процессу обработки 
    # данных с использованием сериализатора, и включает в себя ДЕСЕРИАЛИЗАЦИЮ данных тела запроса, 
    # создание объекта класса сериализатора, валидацию и сохранение сериализованных данных в БД. 
    # СПРАВКА! https://dev-gang.ru/article/kak-ispolzovat-serializatory-v-vebplatforme-django-python-sfru8ukukd/ 

    # Создаем объект класса сериализатора, 
    # который, в том числе, используется и для ДЕСЕРИАЛИЗАЦИИ данных тела ЗАПРОСА (data=request.data) и 
    # далее для валидации сериализованных данных ЗАПРОСА (serialpoint.is_valid())
    # Данные запроса, А НЕ ОБЪЕКТЫ МОДЕЛИ КАК ПРИ сериализации,
    # передаем в сериализатор в виде именованных аргументов, 
    # извлекаемых из тела запроса применением .data

    serialpoint = WorldPointSerializer(data=request.data) # здесь .data для извлечения данных из тела запроса
                                                          # requests.post(url, data={"name": "test", "location": "SRID=28404;POINT(4475177 6061145)"})
    # # ПОЯСНЯЮЩИЙ АНАЛОГ!
    # # Пусть в запросе от клиента к нам поступила такая байтовая строка:
    # import io
    # stream = io.BytesIO(b'{"name":"test_analog","location":"SRID=28404;POINT(4475177 6061545)"}')
    # # Используем JSONParser для десериализации (парсим запрос) !!! (так работает функция decoder()) !!!
    # from rest_framework.parsers import JSONParser
    # parsdata = JSONParser().parse(stream) # ДЕСЕРИАЛИЗУЕМ
    # # print(parsdata) >>> {'name': 'test_analog', 'location': 'SRID=28404;POINT(4475177 6061545)'}
    # serialpoint = WorldPointSerializer(data=parsdata) # Создаем объект класса сериализатора
    # serialpoint.is_valid() # Проверяем на валидность
    # location_data = parsdata.get('location')
    # name = parsdata.get('name')
    # pnt = GEOSGeometry(location_data)  
    # serialpoint.validated_data['location'] = pnt # Получаем доступ к проверенным (валидным) данным
    # serialpoint.validated_data['name'] = name # Получаем доступ к проверенным (валидным) данным
    # serialpoint.save() # Сохраняем в БД
    # return Response(serialpoint.data) # Возвращаем клиенту

    # Проверяем данные на валидность (соответствуют ли они ожидаемой структуре и правилам)
    if serialpoint.is_valid():
        # Если данные валидны, извлекаем название точки и сохраняем их в БД
        location_data = request.data.get('location')  # Извлекаем данные о местоположении
        name = request.data.get('name')  # Извлекаем название точки
        pnt = GEOSGeometry(location_data)  # Создаем объект GEOSGeometry из данных о местоположении
        serialpoint.validated_data['location'] = pnt  # Присваиваем объект GEOSGeometry полю 'местоположение'
        serialpoint.validated_data['name'] = name  # Присваиваем название точки полю 'name'
        # "validated_data (проверенные данные)" в Python используется в контексте сериализации данных. 
        # Когда данные проходят процесс валидации веб-формы или API запроса, 
        # они могут быть доступны через "validated_data". 
        # В этом случае, "serialpoint.validated_data['location'] = pnt" указывает на 
        # присвоение значения переменной "pnt" для ключа "location" в словаре "validated_data". 
        # Это часто используется в контексте обработки и валидации веб-форм или HTTP запросов 
        # во фреймворках, таких как Django REST framework.
        serialpoint.save()  # После успешной валидации, этот метод сохраняет данные, 
        # которые были сериализованы, в базе данных.
        return Response(serialpoint.data)
    else:
        return Response({'error': 'Нет действительных данных POST', 'details': serialpoint.errors}, status.HTTP_404_NOT_FOUND)

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
    
    # извлечение координат точек из БД и введенных пользователем их имен
    # points, points_name = zip(*[(point.location.coords, point.name) for point in WorldPoint.objects.all()])
    # код выше дает ошибку распаковки * при отсутствии каких либо данных на карте
    # но нам нужно как можно меньше обращаться к БД поэтому 
    # выполняем запрос к базе данных всего лишь один раз и извлекаем все точки
    all_points = WorldPoint.objects.all()

    # Используем list comprehensions для извлечения координат и имен точек
    points = [point.location.coords for point in all_points]
    points_name = [point.name for point in all_points]

    # извлечение значения поправки направления из тела запроса (десериализация request.data)
    serialline = WorldLineSerializer(data=request.data)
    # проверка (влияние помех в канале передачи данных) данных на валидность перед записью в БД
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

            myname = f'Ориентир: {points_name[cnt + 0]} - ориентир: {points_name[cnt + 1]}'
            
            # Избавляем базу данных от дубликатов
            # Для того чтобы код проверял на уникальность данные 
            # и не записывал их в базу данных, если они одинаковы можно 
            # воспользоваться методом get_or_create() модели для того, 
            # чтобы проверить наличие записи с такими же данными в базе данных
            
            try:
                created = WorldLine.objects.get_or_create(name=myname, azimuth=res[0], pn=float(pn), distance=res[1], location=new_line)
                # Данные уже существуют в базе данных, не записываем их повторно
                if not created:
                    # Если объект уже существует, проводим необходимые операции
                    # например, обрабатываем сообщение или выполняем другие действия (пока заглушим)
                    pass 
            # Если такой записи нет, продолжаем выполнение    
            except WorldLine.DoesNotExist:

                # создаем структуру данных (словарь) для сериализации
                dictpost = dict(name=myname, azimuth=res[0], pn=float(pn), distance=res[1], location=new_line)
                # (параметру запроса data присваеваем словарь dictpost, передаваемый в теле запроса)
                
                # Сериализуем и проверяем на валидность перед записью в БД
                seriallinepost = WorldLineSerializerPost(data=dictpost)
                if seriallinepost.is_valid():
                    seriallinepost.save()
                else:
                    # возвращаем ответ с ошибкой 404 (Not Found) с сообщением об ошибке и 
                    # дополнительными деталями ошибок валидации, предоставляемыми seriallinepost.errors.
                    return Response({'error': 'No valid data POST', 'details': seriallinepost.errors}, status=status.HTTP_404_NOT_FOUND)
                    # Параметр status=status.HTTP_404_NOT_FOUND используется для установки кода статуса HTTP в ответе КЛИЕНТУ. 
                    # В данном случае, status.HTTP_404_NOT_FOUND представляет стандартный HTTP-статус "404 Not Found", 
                    # который указывает на то, что запрошенный ресурс не был найден на сервере.

                # Ошибка ".DoesNotExist" возникает в Django, когда запрашиваемый объект не существует в базе данных. 
                # Это исключение возникает в том случае, если используется метод, который предполагает наличие объекта, 
                # но такой объект не найден.

                # Например, при работе с моделями Django, при попытке получить объект по определенным 
                # критериям (например, использованием метода get()), если объект с такими критериями не найден в базе данных, 
                # возникнет исключение ".DoesNotExist".

                # В обработчике исключений можно использовать ".DoesNotExist" для перехвата данной ошибки и выполнении 
                # определенных действий в зависимости от ситуации, например, создании нового объекта вместо обращения 
                # к несуществующему.

        
        # Заполняем таблицу связей 
        # Получаем id экземпляров модели WorldLine
        idlins = [lin.id for lin in WorldLine.objects.all()]

        listpointinline = []

        # С помощью транзакции обеспечиваем целостность данных
        # ПОЧИТАТЬ ПРО АТАМАРНОСТЬ https://habr.com/ru/articles/252563/
        with transaction.atomic():
            # проходим по каждой линии в соответствии с ее id
            for idlin in idlins:
                line = WorldLine.objects.get(id=idlin)
                
                # и ищем точки с которыми она пересекается location__intersects
                # где location - поле с геометрией __intersects - метод поиска пересечений
                pnts_intersect = WorldPoint.objects.filter(location__intersects=line.location)
                
                # Если количество пересечений НЕ два это означает, 
                # что одна из точек в админке удалена, 
                # удаляем старую линию из базы данных (ориентира то нет)
                if pnts_intersect.count() == 2:
                    for pnt_intersect in pnts_intersect:
                        # формируем список со вложенными словарями пересечений
                        # это нужно чтобы сформировать связи между конкретной линией и 
                        # точками с которыми она пересекается
                        data = {'mypoints': pnt_intersect.id, 'mylines': line.id}
                        listpointinline.append(data)
                else:
                    # Если количество пересечений не равно двум, удаляем линию
                    line.delete()

                # Использование конструкции with transaction.atomic() в Django обеспечивает 
                # выполнение операций баз образом, который гарантирует атомарность операций, 
                # целостность базы данных и избегание проблем конкурентного доступа к данным.

                # Когда блок кода завершается без исключений, все операции внутри with transaction.atomic() 
                # выполняются и фиксируются в базе данных как единое целое. Если происходит исключение в блоке кода, 
                # то Django откатывает все изменения, внесенные в базу данных во время выполнения этого блока, 
                # чтобы гарантировать целостность данных.

                # Таким образом, использование transaction.atomic() помогает избежать непредвиденных изменений 
                # в базе данных и обеспечивает целостность данных при выполнении нескольких операций.

        # Сохраняем все записи одновременно после цикла, формируя таблицу N:M
        # Проверяем наличие данных в listpointinline перед использованием сериализатора
        # Если лист содержит данные сериализуем проверяем на валидность и записываем их в БД
        if listpointinline: 
            serialpointinline = PointInLineSerializer(data=listpointinline, many=True)
            if serialpointinline.is_valid(raise_exception=True):
                serialpointinline.save()
            else:
                # Эта ошибка появляется когда в списке одна точка пересечения с линией (так как вторую точку мы удалили)
                # в таком случае данные не пройдут проверку на валидность эту ошибку нужно обработать 
                # чтобы выполнение запроса не завершилось кодом 400
                return Response({'error': 'Invalid data N:M:', 'details': serialpointinline.errors}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serialline.data) 
    else:
        Response({'error': 'Invalid data поступившие в теле запроса POST', 'details': serialline.errors}, status=status.HTTP_404_NOT_FOUND)

# - - - - - - - - - - - - - - -
# Создаем обработчик для формирования  
# GeoJSON для визуализации в браузере с помощью Leaflet

def get_context_data(request):
    # сериализация (представляет собой процесс преобразования объекта модели 
    # в форму (объект класса сериализатора (в данном случае geojson-строку)), 
    # пригодную для передачи по проводам и сохранения в БД)

    # Объекты модели, для передачи по проводам и сохранения, нужно СЕРИАЛИЗОВЫВАТЬ - преобразовывать в байт-код (json-строку - поток)
    
    # Забираем из БД предварительно сериализовав данные (хорошо бы еще на валидность потом поверить)
    data_geojson_str_pnt = serialize('geojson', WorldPoint.objects.all(),
            geometry_field='location',
            fields=('name', 'location',))
    data_geojson_str_line = serialize('geojson', WorldLine.objects.all(),
            geometry_field='location',
            fields=('name', 'azimuth', 'pn', 'distance', 'location',))
    
    # десериализация (преобразование серриализованныех данныех (потока) из json строки обратно в структуру словаря python  (str->dict))
    # с предварительной проверкой на валидность
    try:
        validpoint = json.loads(data_geojson_str_pnt)
        validline = json.loads(data_geojson_str_line)
    except json.JSONDecodeError:
        return Response({'error': 'No valid GeoJSON data.'}, status=status.HTTP_400_BAD_REQUEST)
        # В этом случае, при ошибке парсинга JSON будет возвращен ответ с сообщением "No valid GeoJSON data" 
        # и кодом статуса HTTP 400 Bad Request. Это поможет понять клиенту, что отправленные данные 
        # не соответствуют требуемому формату.
    
    context = {
        'context_pnt': validpoint,
        'context_line': validline,
        }
      
    # передаем контекст в шаблон map.html
    return render(request, 'map.html', context)


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


    

