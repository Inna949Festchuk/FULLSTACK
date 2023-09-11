from datetime import datetime
from demo.models import Car
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

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
# Создаеем обработчик для создания новой записи в таблице Car
def create_car(request):
    # Новая запись в таблице - это экземпляр модели Car
    сar = Car(brand='demo', model='demo', color='demo')
    сar.save() # сохраняем запись в БД
    return HttpResponse(f'Новая машина: {сar.brand}, {сar.model}')
    