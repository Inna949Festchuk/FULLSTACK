from django.urls import path
from geoapp.views import (
    map_view,
    add_trek,
    create_point,
    view_inc_person,
    web_inc_person,
    )

app_name = 'geoapp'

urlpatterns = [
    path('create_point/', create_point),
    # - - - - - - - - - - - - - - -
    # Создаем путь к шаблону карты туриста
    path('map/', map_view),
    # - - - - - - - - - - - - - - -
    # возвращаем маршруты
    path('trek/', add_trek),
    # Возвращаем задачи персоналу
    path('task/', view_inc_person),
    # Создаем путь к шаблону карты персонала
    path('webtask/', web_inc_person),

]