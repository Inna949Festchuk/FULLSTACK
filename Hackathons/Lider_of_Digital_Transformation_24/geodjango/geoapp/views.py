from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from geoapp.models import (
    ImportTrek, 
    ImportTrekLine, 
    ImportInc,
    Person,
    IncInPerson,
    )
from rest_framework.response import Response
from rest_framework import status # Отображаем ошибки 404 на странице
from django.contrib.gis.geos import GEOSGeometry
from geoapp.serializers import ImportIncSerializer
from django.core.serializers import serialize, deserialize
from django.contrib.gis.geos import GEOSGeometry

import json

# Функция запуска тестовой странички с картой
def map_view(request):

    # Забираем из БД предварительно сериализовав данные
    trek_pnt = serialize('geojson', ImportTrek.objects.all(),
            geometry_field='location',
            fields=('name', 'location',))
        
    trek_lines = serialize('geojson', ImportTrekLine.objects.all(),
            geometry_field='location',
            fields=('name', 'azimuth', 'pn', 'distance', 'location',))
    
    try:
        valid_point_trek = json.loads(trek_pnt)
        valid_line_trek = json.loads(trek_lines)
        
    except json.JSONDecodeError:
        return Response({'error': 'No valid GeoJSON data.'}, status=status.HTTP_400_BAD_REQUEST)
    
    context = {
        'context_point_trek': valid_point_trek,
        'context_lines_trek': valid_line_trek,
        }
      
    # передаем контекст в шаблон map.html
    return render(request, 'map.html', context)

# эндпоинт добавления выдачи маршрутов
@api_view(['GET'])
def add_trek(request):
    '''
    import requests
    url = "http://127.0.0.1:8000/api/trek/"
    response = requests.post(url)
    response.json()
    '''

    # Забираем из БД предварительно сериализовав данные
    trek_pnt = serialize('geojson', ImportTrek.objects.all(),
            geometry_field='location',
            fields=('name', 'location',))
        
    trek_lines = serialize('geojson', ImportTrekLine.objects.all(),
            geometry_field='location',
            fields=('name', 'azimuth', 'pn', 'distance', 'location',))
    
    try:
        valid_point_trek = json.loads(trek_pnt)
        valid_line_trek = json.loads(trek_lines)

    except json.JSONDecodeError:
        return Response({'error': 'No valid GeoJSON data.'}, status=status.HTTP_400_BAD_REQUEST)
    
    context = {
        'context_point_trek': valid_point_trek,
        'context_lines_trek': valid_line_trek,
        }
    
    # print(context)
    return Response(context)

    
# сервис добавления событий в базу данных    
@api_view(['POST'])
def create_point(request): 
    '''
    import requests
    url = "http://127.0.0.1:8000/api/create_point/"
    response = requests.post(url, data={"name": "test", "location": "SRID=28404;POINT(4475177 6061145)"})
    response.json()
    '''

    # Создаем экземпляр класса сериализатора
    serialinc = ImportIncSerializer(data=request.data)
    if serialinc.is_valid():
        # Если данные валидны, извлекаем данные инцидента и сохраняем их в БД
        valid_data = serialinc.validated_data  # Извлечение валидированных данных один раз
        location_data = valid_data['location'] # Извлекаем данные о местоположении
        name = valid_data['name'] # Извлекаем название точки
        pnt = GEOSGeometry(location_data)  # Создаем объект GEOSGeometry из данных о местоположении
        # Создаем объекты в БД если Данные уже существуют в базе данных, не записываем их повторно
        ImportInc.objects.get_or_create(name=name, location=pnt)
        # Если нужно вернуть в запросе какие-то данные bз БД (например)
        # data = ImportIncSerializer(ImportInc.objects.all(), many=True)
        # return Response(data.data)
        return Response('Данные переданы службам реагирования! С Вами свяжется оператор.')
    return Response('Эти данные уже были переданы ранее') 
    # return Response({'error': 'Нет действительных данных POST', 'details': serialinc.errors}, status.HTTP_404_NOT_FOUND)


# Запускаем тестовую страничку служб реагирования
def web_inc_person(request):
    context = {
        
        }
    return render(request, 'inc.html', context)

# Получаем данные из БД для странички служб реагирования
@api_view(['GET'])
def view_inc_person(request):
    '''
    mport requests
    url = "http://127.0.0.1:8000/api/task/"
    response = requests.post(url)
    response.json()
    {
    'person_data': [
            {
                'name': 'Имя персоны',
                'incidents': ['Инцидент 1', 'Инцидент 2', ...]
            },
            {
                'name': 'Другое имя персоны',
                'incidents': ['Другой инцидент 1', 'Другой инцидент 2', ...]
            },
            # ... другие записи о персонах и их инцидентах
        ]
    }
    '''

    data = []
    persons = Person.objects.all()
    for person in persons:
        person_data = {
            'person_name': person.person_name,
            'incidents': []
        }
        incidents = IncInPerson.objects.filter(person=person)
        for incident in incidents:
            incident_data = {
                'name': incident.incendent.name,
                'location': {
                    'latitude': incident.incendent.location.y,
                    'longitude': incident.incendent.location.x
                }
            }
            person_data['incidents'].append(incident_data)
        data.append(person_data)
    return JsonResponse(data, safe=False)



    











