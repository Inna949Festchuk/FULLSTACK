from django.contrib import admin

# Register your models here.

from .models import Person, Car, Product, Order, OrderPositions

# Создаем админ класс для каждой модели 
# и регистрируем его путем применения декоратора @admin.register()

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

# Создаем инлайнмодель
class OrderPositionInline(admin.TabularInline):
    # указываем модель которая будет встраиваться
    model = OrderPositions
    extra = 3 # Количиство строк встраиваемой таблички если 0 то новых строк не будет а
    # в админке нужно будет нажать на + для их добавления

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price',
        'category',
    ]
    list_filter = [
        'category',
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
    ]
    # Перечисляем используемые инлайны
    # Инланы позволяют встраивать в текущее отображение админки 
    # другое отображение
    inlines = [
        OrderPositionInline,
    ]
