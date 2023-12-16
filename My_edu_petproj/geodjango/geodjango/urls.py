"""Geodjango URL -конфигурация

Список `urlpatterns маршрутирует URL -адреса для просмотров.Для получения дополнительной информации см.:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Примеры:
Функциональные представления
    1. Добавьте импорт: из видов импорта MY_APP
    2. Добавить URL в urlpatterns: path ('', views.home, name = 'Home')
Классовые взгляды
    1. Добавьте импорт: от other_app.views Import Home
    2. Добавьте URL в urlpatterns: path ('', home.as_view (), name = 'home')
В том числе еще один urlConf
    1. Импорт функции include (): из импорта django.urls include, path
    2. Добавить URL в urlpatterns: path ('blog/', include ('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('geoapp.urls')),  # подключаем маршруты из приложения measurement
]

# Создайте пользователя-администратора
# python manage.py createsuperuser
