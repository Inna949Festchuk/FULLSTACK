from django.contrib import admin

# Register your models here.

from .models import Person, Car

# Создаем админ класс для каждой модели 
# и регистрируем его путем применения декоратора

# в браузерен ввести /admin

@admin.register(Car)
class CarAdmin(admin.ModelAdmin): 
    # указываем порядок отоюражения столбцов в админ. панеле
    list_display = [
        'id',
        'brand',
        'model',
        'color',
    ]
    pass
    # для отображения выборки создаем лист-фильтр
    list_filter = [
        'brand',
        'model',
    ]

@admin.register(Person)
class Person(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'car',
    ]
