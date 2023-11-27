# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

# import statistics
# from rest_framework.decorators import api_view
# from .models import Sensor, Measurement
# from rest_framework.response import Response
# from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer
# from rest_framework.generics import RetrieveAPIView
# from rest_framework import generics

# # получение датчиков
# @api_view(['GET'])
# def show_sensors(request):
#     sensors = Sensor.objects.all()
#     data = SensorSerializer(sensors, many=True)
#     return Response(data.data)

# # создание датчика
# @api_view(['POST'])
# def create_sensor(request):
#     name = request.GET.get('name', 'No name')
#     description = request.GET.get('description', 'No description')
#     Sensor(name=name, description=description).save()
#     return Response({'status': 'sensor was added'})

# # обновление датчика
# @api_view(['PATCH'])
# def patch_sensor(request):
#     name = request.GET.get('name', 'No name')
#     new_name = request.GET.get('new_name', 'No name')
#     description = request.GET.get('description', 'No description')
#     Sensor.objects.filter(name=name).update(name=new_name, description=description)
#     return Response({'status': 'sensor was patched'})

# # Добавление измерений 
# @api_view(['POST'])
# def create_measurement(request):
#     # получаемое из параметра запроса целочисленное значение sensor, 
#     # должно быть экземпляром класса Sensor. Поэтому необходимо создать 
#     # экземпляр Sensor выборав его по id=sensor, 
#     # а только затем передать объекту Measurement.
#     sensor = request.GET.get('sensor', 'No sensor')
#     sensor_id = Sensor.objects.get(id=sensor)
#     temperature = request.GET.get('temperature', 'No temperature')
#     Measurement(sensor=sensor_id, temperature=temperature).save()
#     return Response({'status': 'measurement was added'})


# # Получение информации по <pk> датчика с применением класса RetrieveAPIView
# class SensorView(RetrieveAPIView):
#     queryset = Sensor.objects.all()
#     serializer_class = SensorDetailSerializer


# # Просмотр всех измерений с применением класса дженериков ListCreateAPIView
# class MeasurementListView(generics.ListCreateAPIView):
#     queryset = Measurement.objects.all()
#     serializer_class = MeasurementSerializer


# - - - - - - - - - - -
# ВТОРОЙ ВАРИАНТ
# - - - - - - - - - - -

# ДЖЕНЕРИКИ
from rest_framework.generics import ( 
    ListAPIView, 
    CreateAPIView,
    RetrieveAPIView,
)
# МИКСИНЫ
from rest_framework.mixins import ( 
    CreateModelMixin, # миксин прредоставляет .create(request, *args, **kwargs)метод, 
                    # реализующий создание и сохранение нового экземпляра модели.
    UpdateModelMixin, # миксин предоставляет .update(request, *args, **kwargs)метод, 
                    # реализующий обновление и сохранение существующего экземпляра модели.
                    # Также предусмотрен .partial_update(request, *args, **kwargs) 
                    # с необязательными для заполнения всеми полями
)
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


# получение списка датчиков с помощью дженерика ListAPIView,
# создание датчика с помощью миксина CreateModelMixin
# измегнение датчика с помощью миксина UpdateModelMixin
class SensorAPIView(ListAPIView, CreateModelMixin, UpdateModelMixin):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    # lookup_field = 'name' - если нужно искати не по <pk>

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# Добавление измерения температуры к датчику с примененипем дженерика CreateAPIView
class MeasurementAPIView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


# Получение информации по <pk> датчика с применением дженерика RetrieveAPIView
class SensorViewPK(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer