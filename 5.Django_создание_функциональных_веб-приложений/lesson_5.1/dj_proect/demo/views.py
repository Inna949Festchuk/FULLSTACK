from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

# именно так надо импортировать настройки из модуля settings.py
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
# (в веб-браузере ввести hello/?name=Sacha&age=22)
def hello(request):
    name = request.GET.get('name')
    age = int(request.GET.get('age', 20))
    print(age)
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
class DateConverter: # Класс для конвертации
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'
    # Конвертируем из строки в объект Python
    def to_python(self, value: str) -> datetime:
        return datetime.strptime(value, self.format)
    # Конвертируем из объекта Python в строку
    def to_url(self, value: datetime) -> str:
        return value.strftime(self.format)

def user_report(request, id: int, dt):
   # больше никакой валидации в обработчиках
   # сразу правильные типы и никак иначе
   return HttpResponse(f'{id}, {dt}')

def team_report(request, id: int, dt):
   return HttpResponse(f'{id}, {dt}')

# Валидация — это процесс проверки данных различных типов 
# по критериям корректности и полезности для 
# конкретного применения.
