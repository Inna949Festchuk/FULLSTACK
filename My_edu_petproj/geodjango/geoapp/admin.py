# from django.contrib import admin
from django.contrib.gis import admin
from .models import (
    # WorldBorder, 
    # Tile,
    WorldPoint,
    WorldLine,
    # PointInLine,
)
# from .models import Zipcode, Elevation

# Register your models here.
# @admin.register(Zipcode)
# class Zipcode(admin.ModelAdmin):
#     list_display = [
#         'code', 'poly',
#         ]

# @admin.register(Elevation)
# class Elevation(admin.ModelAdmin):
#     list_display = [
#         'name', 'rast',
#         ]

# admin.site.register(WorldBorder, admin.ModelAdmin)

# @admin.register(WorldBorder)
# class WorldBorderAdmin(admin.OSMGeoAdmin):
#     list_display = ('name', 'lon', 'lat')


# Регистрируем модель точек в админпанели GeoDjango
@admin.register(WorldPoint)
class WorldPointAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('name', )
    # Скрыть отображение поля в админке
    # exclude = ('myline',)


@admin.register(WorldLine)
class WorldLineAdmin(admin.GISModelAdmin):
    list_display = ('name', 'azimuth', 'pn', 'distance', )
    # Отображение полей с атрибутом только для чтения
    readonly_fields = ('azimuth', 'pn', 'distance', )
    # Скрыть отображение поля в админке
    exclude = ('name', )


# @admin.register(PointInLine)
# class PointInLineAdmin(admin.GISModelAdmin):
#     # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
#     list_display = ('mypoints', 'mylines', )


# @admin.register(Tile)
# class TileAdmin(admin.GISModelAdmin):
#     list_display = ('zoom_level', 'tile_column', 'tile_column', 'tile_row', 'tile_data', 'geom', ) 
   
# # forms используется для определения собственной формы, admin 
# # для работы с административной панелью
# from django import forms
# from django.contrib.gis import admin as geoadmin
# # Cпособ отключить редактирование поля locations в административной панели GeoDjango. 
# # Нужно переопределить форму административной панели, чтобы управлять отображением и доступностью полей.
# class WorldLineForm(forms.ModelForm):
#     class Meta:
#         model = WorldLine
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(WorldLineForm, self).__init__(*args, **kwargs)
#         instance = kwargs.get('instance') # извлечение экземпляра объекта модели
#         # В контексте определения формы административной панели Django, instance 
#         # обычно представляет текущий экземпляр объекта модели, с которым работает форма.
#         if instance:
#             self.fields['location'].widget.attrs['readonly'] = True  # Установка поля "location" как только для чтения
           
# class WorldLineAdmin(geoadmin.GISModelAdmin):
   
#     list_display = ('azimuth', 'pn', 'distance', )
    
#     readonly_fields = ('azimuth', 'pn', 'distance', )

# admin.site.register(WorldLine, WorldLineAdmin)