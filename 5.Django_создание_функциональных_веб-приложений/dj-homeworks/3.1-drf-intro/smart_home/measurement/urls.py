from django.urls import path
from measurement.views import (
    create_sensor, 
    patch_sensor, 
    show_sensors,
    create_measurement,
    SensorView, 
    MeasurementListView,
)

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    # получение датчиков
    path('show_sensors/', show_sensors),
    # создание датчика
    path('create_sensor/', create_sensor),
    # обновление датчика
    path('patch_sensor/', patch_sensor),
    # добавление измерения
    path('measurement/', create_measurement),
    # получение конкретного датчика по его id <pk>
    path('sensors/<pk>/', SensorView.as_view()),
    # просмотр всех измерений через класс дженерика
    path('measurement_class/', MeasurementListView.as_view()),
]