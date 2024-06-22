# Это скрипт загрузки файла формата *.json в базу данных postgresql

from django.core.management.base import BaseCommand
from geoapp.models import ImportTrek
from django.contrib.gis.geos import GEOSGeometry, Point

from sympy import Point
from geoapp.models import ImportTrek, ImportTrekLine
from django.contrib.gis.geos import GEOSGeometry, LineString
from geoapp.serializers import ImportTrekLineSerializerPost, ImportTrekSerializer, PointInLineSerializer
from django.contrib.gis.geos import GEOSGeometry
from math import atan2, degrees, radians, sin, cos, sqrt

# Обеспечиваем атамарность при работе с данными БД (читай ниже)
from django.db import transaction
# - - - - - - - - - - - - - - -

import json
import math


class Command(BaseCommand):
    '''
    python manage.py import_json -c
    Класс дает возможность создания собственной терминальной команды
    импорта в БД даных из формата *.json создания точечных объектов и линейных объектов,
    а также расчета азимута каждой линии и ее длины в парах шагов для ориентирования на местности по компасу
    '''
    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            action='store_true',
            default=False,
            help=''
        )

    def handle(self, *args, **options):

        if options['c']:     

            with open('geoapp\data\DataSource.json') as f:
                data = json.load(f)

            for ft in data['features']:
                geom_L = json.dumps(ft['geometry']['coordinates'][0])
                geom_B = json.dumps(ft['geometry']['coordinates'][1])
                geom = GEOSGeometry(f'SRID=4326;POINT({geom_L} {geom_B})')
                name = ft['id']
                
                # Избавляем базу данных от дубликатов
                try:
                    created = ImportTrek.objects.get_or_create(name=f'Точка: {name}', location=geom)
                    # Данные уже существуют в базе данных, не записываем их повторно
                    if not created:
                        pass 
                # Если такой записи нет, продолжаем выполнение    
                except:
                
                    # создаем структуру данных (словарь) для сериализации
                    dictpost = dict(name=f'Точка: {name}', location=geom)

                    # Сериализуем и проверяем на валидность перед записью в БД
                    seriallpoint = ImportTrekSerializer(data=dictpost)
                    if seriallpoint.is_valid():
                        seriallpoint.save()
                    else:
                        print('No valid data') 
                 

            def Am(lon1, lat1, lon2, lat2, Pn=0):
                point1 = Point(lon1, lat1)
                point2 = Point(lon2, lat2)
                # переводим градусы в радианы
                lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                azimuth = atan2(sin(dlon) * cos(lat2),
                                cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon))
                azimuth = degrees(azimuth)
                # перевод азимута в диапазон от 0 до 360 градусов
                a = (azimuth + 360) % 360

                # Преобразование в метры
                R = 6371000.0  # Радиус Земли в метрах
                S = R * math.acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)) / 1.5

                Am_degre = a - Pn
                # Пересчитываем десятичные градусы в градусы, минуты, секунды
                Am_grad = int(Am_degre)
                Am_min = int(60 * (Am_degre - Am_grad))
                Am_sec = round(60 * (60 * (Am_degre - int(Am_degre)) - Am_min), 1)
                # Объединяем все в одну строку
                Am = ''.join([str(Am_grad)+" град ", str(Am_min)+" мин ", str(Am_sec)+' с'])
                # Округляем п.ш.
                S = f'{S:.1f} п.ш.'

                # zone = math.ceil((lon1) / 6) + 1
                
                return Am, S

            
            # извлечение координат точек из БД 
            
            points = [point.location.coords for point in ImportTrek.objects.all()]
            points_name = [point.name for point in ImportTrek.objects.all()]

            # если данных нет принять по-умолчанию ПН=0
            pn = 0

            for cnt in range(len(points) - 1):
                # рассчет азимута и расстояния в пар-шагах
                res = Am(points[cnt][1], points[cnt][0], points[cnt + 1][1], points[cnt + 1][0], Pn=float(pn))
                
                # создание линий на основе извлекаемых точек
                new_line = LineString(points[cnt], points[cnt + 1], srid=4326)
                myname = f'{points_name[cnt + 0]} - {points_name[cnt + 1]}'

                # Избавляем базу данных от дубликатов
                try:
                    created = ImportTrekLine.objects.get_or_create(name=myname, azimuth=res[0], pn=float(pn), distance=res[1], location=new_line)
                    # Данные уже существуют в базе данных, не записываем их повторно
                    if not created:
                        pass 
                # Если такой записи нет, продолжаем выполнение    
                except:
                
                    # создаем структуру данных (словарь) для сериализации
                    dictpost = dict(name=myname, azimuth=res[0], pn=float(pn), distance=res[1], location=new_line)

                    # Сериализуем и проверяем на валидность перед записью в БД
                    seriallinepost = ImportTrekLineSerializerPost(data=dictpost)
                    if seriallinepost.is_valid():
                        seriallinepost.save()
                    else:
                        print('No valid data') 
                    
            
            # Заполняем таблицу связей 
            # Получаем id экземпляров модели WorldLine
            idlins = [lin.id for lin in ImportTrekLine.objects.all()]

            listpointinline = []

            # С помощью транзакции обеспечиваем целостность данных
            with transaction.atomic():
                # проходим по каждой линии в соответствии с ее id
                for idlin in idlins:
                    line = ImportTrekLine.objects.get(id=idlin)

                    # и ищем точки с которыми она пересекается location__intersects
                    # где location - поле с геометрией __intersects - метод поиска пересечений
                    pnts_intersect = ImportTrek.objects.filter(location__intersects=line.location)
                    
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
                    print('Invalid data N:M:')
        else:
            print('Введите python manage.py import_json -c')
