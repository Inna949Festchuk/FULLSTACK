## lesson 5.2 Обработка запросов и шаблоны

### Учебный материал:
- **Введение в занятие "Обработка запросов и шаблоны"**
- **Работа с конфигом Django**

Конфигурация Django задается в файле `settings.py,` который можно найти в главном пакете проекта. В этом файле уже описано множество переменных, на которые Django опирается при работе. [Дополнительная информация про конфигурацию Django](https://docs.djangoproject.com/en/3.2/topics/settings/)
В `settings.py` можно добавлять свои собственные переменные и потом пользоваться ими в любом удобном месте.
Для получения значений из конфигурации, необходимо обращаться к полям в объекте *settings*:

```python
# именно так надо импортировать настройки
from django.conf import settings
from django.http import HttpResponse

def hello_view(request): 
    msg = f'Свяжитесь с админом {settings.CONTANCT_EMAIL}' 
    return HttpResponse('Всем привет! Я Django! ' + msg)
```

- **Параметры запросов**
- **Конвертеры маршрутов в Django** ([Статья по теме](https://habr.com/ru/companies/yandex_praktikum/articles/541068/))

Конвертеры маршрутов в Django существуют не для всех типов данных.

[Стандартные конвертеры описаны в документации](https://docs.djangoproject.com/en/3.2/topics/http/urls/#path-converters)

Django помимо стандартных конвертеров предоставляет возможность создать **свой конвертер** и описать правила конвертации так, как угодно.

Для этого надо сделать два шага:
- Описать класс конвертера.
- Зарегистрировать конвертер.

**Класс конвертера** — это класс с определённым набором атрибутов и методов, описанных в документации (на мой взгляд, несколько странно, что разработчики не сделали базовый абстрактный класс). Сами требования:

1. Должен быть атрибут **regex**, описывающий регулярное выражение для быстрого поиска требуемой подпоследовательности. Чуть позже покажу, как он используется.
2. Реализовать метод **def to_python(self, value: str)** для конвертации из строки (ведь передаваемый маршрут — это всегда строка) в объект python, который в итоге будет передаваться в обработчик.
3. Реализовать метод **def to_url(self, value) -> str** для обратной конвертации из объекта python в строку (используется, когда вызываем django.urls.reverse или тег url).
Класс для конвертации даты будет выглядеть так:

```python
class DateConverter:
   regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'

   def to_python(self, value: str) -> datetime:
       return datetime.strptime(value, '%Y-%m-%d')

   def to_url(self, value: datetime) -> str:
       return value.strftime('%Y-%m-%d')
```
Вынесем формат даты в атрибут для упрощения поддержки конвертера:
```python
class DateConverter:
   regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
   format = '%Y-%m-%d'

   def to_python(self, value: str) -> datetime:
       return datetime.strptime(value, self.format)

   def to_url(self, value: datetime) -> str:
       return value.strftime(self.format)
```
По итогу описания класса можно зарегистрировать его как конвертер. Для этого в функции **register_converter** надо указать описанный класс и название конвертера, чтобы использовать его в маршрутах.
```python
from django.urls import register_converter
register_converter(DateConverter, 'date')
```
Опишем маршруты в urls.py:
```python
path('users/<int:id>/reports/<date:dt>/', user_report, name='user_report'),
path('teams/<int:id>/reports/<date:dt>/', team_report, name='team_report'),
```
Теперь гарантируется, что обработчики вызываются только в том случае, если конвертер отработает корректно, а это значит, что в обработчик придут параметры нужного типа:
```python
def user_report(request, id: int, dt: datetime):
   # больше никакой валидации в обработчиках
   # сразу правильные типы и никак иначе
```
- **Введение в шаблоны**
- **Пагинация**
- **Презентация к видео "Обработка запросов и шаблоны"**
- **Тест по теме «Обработка запросов и шаблоны»**
- **Код к занятию (листинг)**

### Дополнительные материалы:

- [Настройка конфигурации для дебаггера в VS Code](../lesson_5.1/debug_config)

- [Курс по django](https://proglib.io/p/kurs-django-chast-1-django-chto-eto-obzor-i-ustanovka-freymvorka-struktura-proekta-2023-07-25)

### [Домашняя работа](../dj-homeworks/1.1-first-project/)

