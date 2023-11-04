## lesson 5.4 Работа с ORM (часть 2)

### Учебный материал:
- **Введение в занятие Работа с ORM (2 часть)**
- **Связи многие-ко-многим**
- **Many-to-many с помощью through**

Когда мы избавились от дублирования информации, удалив свойство products из модели Order, мы лишились возможности напрямую получать доступ к продуктам в заказе.

Косвенно можно получить продукты в заказе так:
```Python
- order_positions = some_order.positions.all()
- order_products = {pos.product for pos in order_positions}
```
Однако такой метод предполагает, что во всех местах, где нам потребуется получить продукты из заказа, придётся писать одинаковый код, что не всегда удобно. Также и в обратную сторону: чтобы найти все заказы, в которых участвует продукт, необходимо написать такой код:
```Python
- product_positions = some_product.positions.all()
- product_orders = {pos.order for pos in product_positions}
```
А ведь в первоначальном варианте, когда Django автоматически создавал связь m2m, было удобнее — было свойство products в классе Order и related_name orders.
На самом деле такую связь можно оставить, просто надо явно указать, что связь будет осуществляться через специальную модель. Тогда Django не будет создавать автоматическую связь m2m, но при этом останутся необходимые свойства:

```Python
class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders', through='OrderPosition')
```
Теперь можно получать продукты из заказа простым способом:
```Python
order_products = some_order.products.all()
```
Аналогично с заказами, в которых участвует продукт:
```Python
product_orders = some_product.orders.all()
```
- **Django Debug Toolbar**

Для удобного мониторинга и отладки проекта можно установить специальную библиотеку - **Django Debug Toolbar**.

[Полное руководство по библиотеке](https://django-debug-toolbar.readthedocs.io/en/latest/index.html)

Чтобы запустить Django Debug Toolbar необходимо выполнить несколько действий:
установить библиотеку:
`pip install django-debug-toolbar`

Настроить переменную `INSTALLED_APPS` в `settings.py`: убедиться, что присутствует приложение `django.contrib.staticfiles` и добавить новое приложение `debug_toolbar` (обязательно добавить его после `django.contrib.staticfiles`):
```Python
INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles',
    # ...
    'debug_toolbar',
]
```
Настроить переменную `STATIC_URL` в `settings.py`:
`STATIC_URL = '/static/'`
Убедиться, что в переменной `TEMPLATES` в `settings.py` параметр `APP_DIRS` установлен в значение `True`
Добавить в переменную `MIDDLEWARE` в `settings.py` в самое начало:
```Python
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]
```
Добавить переменную `INTERNAL_IPS` в `settings.py`:
```Python
INTERNAL_IPS = [
    '127.0.0.1',
]
```
Добавить маршрут в самый конец `urlpatterns` в файле `urls.py`:
```Python
import debug_toolbar
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    ...
    path('__debug__/', include(debug_toolbar.urls)),
]
```
После выполнения всех действий при ответе сервера в браузере справа будет доступен инструмент `Django Debug Toolbar`.

[Пример настроенного проекта](https://github.com/jazzband/django-debug-toolbar/tree/main/example)

- **Презентация к видео "Работа с ORM"**

- **[Код к занятию (листинг)](../DJ_code/orm_advanced)**

### Дополнительные материалы:

- [Настройка конфигурации для дебаггера в VS Code](../lesson_5.1/debug_config)

### [Мой код по материалам занятий](../lesson_5.1/dj_proect/)

### [Домашняя работа](../dj-homeworks/2.2-databases-2/)
