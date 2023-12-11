from datetime import datetime
import random

from .serializers import ComentsSerializer, WeaponSerializer
from demo.models import Car, Person, Order, Coments
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
# API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Weaponts, Avd
from .serializers import WeaponSerializer, AvdSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated # РАЗДЕЛЕНИЕ ДОСТУПА В DRF
# именно так надо импортировать настройки из модуля settings.py
from demo.permissions import IsOnwer # наш permission_class разграничения прав доступа пользователей к ресурсам
from rest_framework.throttling import AnonRateThrottle # троттлинг запросов
from django.conf import settings

# Create your views here.
def index(request):
    return HttpResponse('Hello from django')

def time(request):
    curent_time = datetime.now().time()
    return HttpResponse(f'Time = {curent_time}')

# именно так надо импортировать настройки из модуля settings.py
def hello_view(request): 
    msg = f'Свяжитесь с админом {settings.CONTANCT_EMAIL}' 
    return HttpResponse('Всем привет! Я Django! ' + msg)

# - - - - - - - - - - - - -
# ПАРАМЕТРИЗАЦИЯ ЗАПРОСОВ
# - - - - - - - - - - - - -
# с помощью GET-параметров в запросе 
# (в веб-браузере ввести hello/?name=Sacha&age=22, что представляется словарем
# {name:Sacha, age=22})
def hello(request):
    name = request.GET.get('name')
    age = int(request.GET.get('age', 20))
    print(age) # Тестим принтом
    return HttpResponse(f'Hello its django. Hello its {name} my {age}')

# с помощью URL
# (в веб-браузере ввести sum/2/5)
def sum(request, a, b):
    # result = int(a) + int(b)
    # или если воспользоваться конвертером 
    # см. в url.py то можно так
    result = a + b
    return HttpResponse(f'{a} + {b} = {result}')

# - - - - - - - - - - - - -
# КОНВЕРТОРЫ МАРШРУТОВ
# - - - - - - - - - - - - -
# Статья по теме
# https://habr.com/ru/companies/yandex_praktikum/articles/541068/
# Конвертор лучше вынести в отдельный модуль converters.py
# Смотри видео https://www.youtube.com/watch?v=jjsVHbTBHFw
# (в браузере ввести http://127.0.0.1:8000/users/8/reports/2023-year08-mon30-day/)
class DateConverter: # Класс для конвертации
    regex = r'[0-9]{4}-year[0-9]{2}-mon[0-9]{2}-day' # Выбираем из urlпо этому шаблону
    format = '%Y-year%m-mon%d-day' #Задаем формат даты 
    # Конвертируем из выбранного в соответствии с регулчркой фрагента
    # url-строки в объект Python
    def to_python(self, value: str) -> datetime:
        return datetime.strptime(value, self.format)
    # Конвертируем из объекта Python в строку
    def to_url(self, value: datetime) -> str:
        return value.strftime(self.format)

# Возвращаем строку со сконвертированным значением dt
def user_report(request, id: int, dt):
   # больше никакой валидации в обработчиках
   # сразу правильные типы и никак иначе
   return HttpResponse(f'{id}, {dt}')

def team_report(request, id: int, dt):
   return HttpResponse(f'{id}, {dt}')

# Валидация — это процесс проверки данных различных типов 
# по критериям корректности и полезности для 
# конкретного применения.


# - - - - - - - - - - - - -
# ШАБЛОНЫ
# - - - - - - - - - - - - -
def hello_html(request):
    # Передача параметров в шаблон при помощи контекста
    context = {
        'test': 5,
        'data_list': [1, 5, 8],
        'val': 'hello',
    }
    return render(request, 'demo.html', context) # 'demo.html' - это путь к html-шаблону

# - - - - - - - - - - - - -
# ПАГИНАЦИЯ
# - - - - - - - - - - - - -
# Создадим обработчик, который будет выдавать контент постранично (порциями)
CONTENT = [str(i) for i in range(10000)] # создаем контент, который нужно пагигнировать
def pagi(request):
    # Чтобы предоставить пользователю возможность самому
    # выбирать нужную страницу делай так
    page_number = int(request.GET.get("page", 1))
    # в браузере тогда набирай http://127.0.0.1:8000/pagi/?page=89
    paginator = Paginator(CONTENT, 10)
    # 10 - это число элементов на одной странице
    # Организуем переход на страницу 5
    # page = paginator.get_page(5)
    page = paginator.get_page(page_number)
    # Передаем переменную page в контекст для доступа к ней из шаблона
    context = {
        'page': page
    }
    return render(request, 'pagi.html', context)

# ---------------------------------------------------------------
# ORM
# ---------------------------------------------------------------
# # Создаеем обработчик для создания новой записи в таблице Car
# def create_car(request):
#     # Новая запись в таблице - это экземпляр модели Car
#     сar = Car(brand='demo', model='demo', color='demo')
#     сar.save() # сохраняем запись в БД
#     return HttpResponse(f'Новая машина: {сar.brand}, {сar.model}')
# 
# Cоздание запросов
def create_car(request):
    # Новая запись в таблице - это экземпляр модели Car
    сar = Car(
        brand=random.choice(['B1', 'B2', 'B3']), 
        model=random.choice(['M1', 'М2', 'M3']), 
        color=random.choice(['C1', 'C2', 'C3']),
    )
    сar.save() # сохраняем запись в БД
    return HttpResponse(f'Новая машина: {сar.brand}, {сar.model}')

# 1:М - - - - - - - -
# Создадим обработчик запросов к БД
def list_car(request):
    # # Выборка всех объектов all()
    # car_objects = Car.objects.all() 
    # # Car - модель, objects - менеджер позволяющий управлять всеми объектами в БД,
    # # all() - метод выбирающий все строки из БД
    # # Выборка объектов по условию filter() 
    # # car_objects = Car.objects.filter(brand='B2') 

    # # МОДИФИКАТОРЫ
    # # Выборка объектов по условию filter() содержащих '2'
    # # car_objects = Car.objects.filter(brand__contains='2') 
    # # Модификатор __contains выбирает объекты СОДЕРЖАЩИЕ '2'
    # # car_objects = Car.objects.filter(brand__startswith='2') 
    # # Модификатор __startswith говорит что выборка должна НАЧИНАТЬСЯ с '2'

    # cars = [f'{c.id}. {c.brand}, {c.model}: {c.color} | {c.owners.count()}' for c in car_objects]
    # # c.owners.count() - count() количество владельцев этим авто, можно применять filter()
    # return HttpResponse('<br>'.join(cars)) 
    # # тег <br> это перенос в списке на новую строку

    # Выборка с применением реляционного имени
    # - - - - - - - - - - 
    car_object = Car.objects.get(id=1)
    # Задача: Определить всех собственников авто с id=1
    # Получаем собственников авто с id=1 из связной (1:M)
    # модели Person с помощью related_name
    owners_this_car = car_object.owners.all()
    # Выводим каждого из собственников на основе полученного QuerySet'a
    owner_this_car = [owner_this_car.name for owner_this_car in owners_this_car]
    owner = '<br>'.join(owner_this_car)
    return HttpResponse(f'{car_object.model} -> {owner}')


# Создадим обработчик для модели Person владельцы авто
def create_person(request):
    # Выбираем из БД все авто и создаем для каждой из них владельца
    cars = Car.objects.all()
    for car in cars:
        print(car)
        # Первый вариант
        # Person(name='P', car=car).save()
        # name и car - это поля в таблице
        # Второй вариант
        Person.objects.create(name='P', car=car)
    return HttpResponse('Люди добавлены')

def list_person(request):
    person_objects = Person.objects.all()
    # people = [f'{p.name} -> {p.car}' for p in person_objects]
    # ТАК КАК car - это FK с моделью Car у которой метод __str__ 
    # переопределен на f'{self.brand}, {self.model}: {self.color}'
    # мы получим 
    # >>> Mr Smith -> Mersedes, e5: green
    # Причем можно вывести отдельно поля Car например
    people = [f'{p.name} -> {p.car.color}' for p in person_objects]
    # >>> Mr Smith -> green
    return HttpResponse('<br>'.join(people))

# М:М (занятие 2) - - - - - - - - 
# Создаем обработчик заказов и продуктов
def list_orders(request):
    # orders = Order.objects.all() # Получаем все заказы
    # А если нужно достать продукты с ценой выше 600 рублей то заменяем на строку ниже -->
    orders = Order.objects.filter(positions__product__price__gte=600)
    # Используя модификаторы __ проваливаемся в соответствующие сущности
    # например, у позиции есть продукт, а у продукта есть цена, мы не можем использовать знаки больше
    # или меньше, для этого есть модификаторы __gte - это больше или равно __lte - меньше или равно
    # __gt - строго больше, __lt - строго меньше
    context = {'orders': orders}
    return render(request, 'orders.html', context)

# ---------------------------------------------------------------
# DRF
# ---------------------------------------------------------------

# # Декоратор для преобразования простого обработчика в API-бработчик
# # Параметр декоратора - это тип запроса на который должен отвечать обработчик
# # GET, POST, PUT PATH

@api_view(['GET'])
def demo(requests):
    weaponts = Weaponts.objects.all()
    ser = WeaponSerializer(weaponts, many=True)
    # many=True означает что серриалайзер выдаст нам все объекты weaponts, 
    # а не какой-нибудь один

    # dictdata = {'message': 'Hello, world!'} 
    # Словарь передается в Response без сериализации
    # return Response(dictdata)

    # Объекты модели, для сохранения или передачи,
    # нужно СЕРИАЛИЗОВЫВАТЬ (weaponts -> ser) - 
    # преобразовывать в байт-код (поток) 
    return Response(ser.data) 

    # ser - сериализованные данные (поток)
    # .data - ДЕССИРИЛИЗАЦИЯ (преобразование 
    # серриализованныех данныех (потока) обратно в структуру словаря
# Response - класс аналог HttpResponse но для API обработчика

# # Добавим к обработчику еще и POST запрос
# @api_view(['GET', 'POST'])
# def demo(requests):
#     if requests.method == 'GET':
#         weaponts = Weaponts.objects.all()
#         ser = WeaponSerializer(weaponts, many=True)
#         return Response(ser.data)
#     if requests.method == 'POST':
#         return Response({'status': 'OK'})
    
# # Такую (слишком ветвленую) логику
# # заменяют специальным классом APIView
# class DemoView(APIView):
#     def get(self, request):
#         '''Метод принимающий на вход и запросы GET'''
#         weaponts = Weaponts.objects.all()
#         ser = WeaponSerializer(weaponts, many=True)
#         return Response(ser.data)
#     def post(self, request):
#         '''Метод принимающий на вход и запросы POST'''
#         return Response({'status': 'OK'})

class DemoView(ListAPIView):
    # откуда береем данные передаем в queryset (название переменной не менять)
    queryset = Weaponts.objects.all()
    # с помощью какого сериалайзера превратить объекты модели 
    # в поток и после сохранения или передачи в словарь JSON
    serializer_class = WeaponSerializer
    
    # если нужно реализовать дополнительное поведение
    # делаем это через def post(self, request):
    def post(self, request):
        # Добавляем запись в БД(например создаем НОВЫЙ заказ)
        # Weaponts(power=500, rerity='силища', value=555).save()
        return Response({'status': 'OK'})
    
# Если нужна информация по единственному виду оружия 
# (по id поля <pk> указываемого в пути в urls.py, 
# н-р: path('weapon/<pk>/', WeaponView.as_view()))
class WeaponView(RetrieveAPIView):
    queryset = Weaponts.objects.all()
    serializer_class = WeaponSerializer

# ---------------------------------------------------------------
# CRUD in DRF
# ---------------------------------------------------------------
# ViewSet - позволяет создать и описать сразу все обработчики
# ресурса вместо того чтобы писать отдельные API (создания, удаления коментов и т.д.)
from rest_framework.viewsets import ViewSet, ModelViewSet

# class ComentViewSet(ViewSet):
    
#     # ViewSet выводит список всех объектов данного ресурса (все коментарии)
#     def list(self, request):
#         return Response({'status': 'OK'})

#     # ViewSet выводит какой-то конкретный объект
#     def retrieve(self, request):
#         pass

#     # ViewSet удаления объекта
#     def destroy(self, request):
#         pass

#     # ViewSet обновления объекта
#     def update(self, request):
#         pass

#     # ViewSet создания объекта
#     def create(self, request):
#         pass

# Но в DRF есть еще более удобный ViewSet это ModelViewSet
# в котором все методы ViewSet уже реализованы

class ComentViewSet(ModelViewSet):
    queryset = Coments.objects.all()
    serializer_class = ComentsSerializer
    # после создания сериализаторы регистрируем маршрут к этому классу

    # НАСТРОЙКА ФИЛЬТРАЦИИ (второй способ)
    filter_backends = [
        # DjangoFilterBackend,
        SearchFilter, # это поисковый фильтр
        OrderingFilter, # фильтр упорядочивания данных
    ]
    # фильтрация по параметрам по полям (параметры передаются в GET запросе после ?user=1)
    filterset_fields = ['user', ]

    # поисковая фильтрация по полям
    search_fields = ['text', ] #(в GET указать ?search=то что мы ищем)

    # упорядочивание по полям
    ardering_fields = ['id', 'user', 'text', 'created_at']

    # второй способ настройки пагинации
    pagination_class = LimitOffsetPagination
    # класс имеет два параметра
    # offset - с какого объекта начинать
    # limit - сколько объектов отображать

# ---------------------------------------------------------------
# Разделение доступа in DRF
# ---------------------------------------------------------------


class AvdViewSet(ModelViewSet):
    queryset = Avd.objects.all()
    serializer_class = AvdSerializer
    # РАЗДЕЛЕНИЕ ДОСТУПА
    # Пользователь должен быть АУТЕНТИФИЦИРОВАН И ВЛАДЕТЬ ресурсом
    permission_classes = [
        IsAuthenticated, 
        IsOnwer
        ]
    # IsAuthenticated - требует чтобы пользователь был аутентифицирован то есть представил свой токен
    # IsOnwer - созданный нами permission_class РАЗГРАНИЧЕНИЯ ПРАВ ПОЛЬЗОВАТЕЛЕЙ НА РЕСУРСЫ
    # Включаем тротлинг для анонимных пользователей
    trottle_classes = [AnonRateThrottle]

    # передаем пользователя с соответствующим ему в БД токеном в сериализатор
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # self.request.user # - так как наш User и соответствующий ему токен уже хранятся в БД
        # далее указать в сериалайзере AvdSerializer поле user как read-овое поле