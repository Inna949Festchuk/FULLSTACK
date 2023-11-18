"""
URL configuration for lesson_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo.views import (
    DemoView,
    WeaponView,
    # demo,
    index, 
    time, 
    hello_view,
    hello, 
    sum, 
    user_report, 
    team_report,
    DateConverter,
    hello_html,
    pagi,
    create_car,
    list_car,
    create_person,
    list_person,
    list_orders,
)

# По итогу описания класса можно зарегистрировать его как конвертер. 
# Для этого в функции register_converter надо указать описанный класс и название конвертера, 
# чтобы использовать его в маршрутах.
from django.urls import register_converter
register_converter(DateConverter, 'date') # date - это название нового регистрированного конвертора


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('time/', time),
    path('helloview/', hello_view),
    # - - - - - - - - - - - - -
    # ПАРАМЕТРИЗАЦИЯ ЗАПРОСОВ
    # - - - - - - - - - - - - -
    path('hello/', hello),
    # path('sum/<a>/<b>', sum)
    # воспользуемся конвертером
    path('sum/<int:a>/<int:b>', sum),
    # - - - - - - - - - - - - -
    # КОНВЕРТОРЫ МАРШРУТОВ
    # - - - - - - - - - - - - -
    # Статья по теме
    # https://habr.com/ru/companies/yandex_praktikum/articles/541068/
    path('users/<int:id>/reports/<date:dt>/', user_report, name='user_report'),
    path('teams/<int:id>/reports/<date:dt>/', team_report, name='team_report'),
    # - - - - - - - - - - - - -
    # ШАБЛОНЫ
    # - - - - - - - - - - - - -
    path('hellohtml/', hello_html, name='hello_html'),
    # - - - - - - - - - - - - -
    # ПАГИНАЦИЯ
    # - - - - - - - - - - - - -
    path('pagi/', pagi),
    # ---------------------------------------------------------------
    # ORM
    # ---------------------------------------------------------------
    path('new_car/', create_car),
    # Обработчик запросов к БД
    path('cars/', list_car),
    path('new_person/', create_person),
    path('people/', list_person),
    # ---------------------------------------------------------------
    # ORM 2
    # ---------------------------------------------------------------
    path('orders/', list_orders),
    # ---------------------------------------------------------------
    # DRF
    # ---------------------------------------------------------------
    # path('demo/', demo),
    path('demo/', DemoView.as_view()),
    # .as_view() превращает класс в функцию для возможности его регистрации в urls.py
    # так как идет выборка одного конкретного образца в запросе необходимо
    # указывать идентификатор этого образца, передающегося
    #  в виде параметра pk
    path('weapon/<pk>/', WeaponView.as_view()),
]
