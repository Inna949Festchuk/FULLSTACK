# from django.db import models
from django.contrib.gis.db import models

# # Create your models here.
# class Zipcode(models.Model):
#     code = models.CharField(max_length=5)
#     poly = models.PolygonField()

# class Elevation(models.Model):
#     name = models.CharField(max_length=100)
#     rast = models.RasterField()


# class WorldBorder(models.Model):
#     # Regular Django fields corresponding to the attributes in the
#     # world borders shapefile.
#     name = models.CharField(max_length=50)
#     area = models.IntegerField()
#     pop2005 = models.IntegerField('Population 2005')
#     fips = models.CharField('FIPS Code', max_length=2, null=True)
#     iso2 = models.CharField('2 Digit ISO', max_length=2)
#     iso3 = models.CharField('3 Digit ISO', max_length=3)
#     un = models.IntegerField('United Nations Code')region = models.IntegerField('Region Code')
#     subregion = models.IntegerField('Sub-Region Code')
#     lon = models.FloatField()
#     lat = models.FloatField()

#     # GeoDjango-specific: a geometry field (MultiPolygonField)
#     mpoly = models.MultiPolygonField()

#     # Returns the string representation of the model.
#     def __str__(self):
#         return self.name

# class WorldLine(models.Model):
#     name = models.CharField(max_length=50)
#     lon = models.FloatField()
#     lat = models.FloatField()

#     # GeoDjango-specific: a geometry field (MultiLineString)
#     mline = models.MultiLineStringField()

#     # Returns the string representation of the model.
#     def __str__(self):
#         return self.name

# УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ:
# - - - - - - - - - - - - - - -
# - Задаем переменную среды PATH:
# PATH=/Applications/Postgres.app/Contents/Versions/12/bin/:$PATH
# - удалить БД:
# dropdb test
# - создать БД от USERNAME -U postgres под названием test и сразу подключиться к ней -d
# psql -U postgres -d test
# - установить пароль подключения
# ALTER USER postgres WITH PASSWORD 'admin'
# - - - - - - - - - - - - - - -

class WorldLine(models.Model):
    
    class Meta:
        # изменить название модели в админ панели Django
        verbose_name_plural = 'Схема движеия по азимутам'
        # _plural - автоокончание отключено
        db_table = "lines_model" # название модели в БД
    
    name = models.CharField(max_length=250, default=' - ', blank=True, verbose_name='Название схемы')
    azimuth = models.CharField(max_length=250, default=' - ', blank=True, verbose_name='Значение азимута магнитного')
    pn = models.FloatField(default=0, blank=True, verbose_name='Поправка направления')
    distance = models.CharField(max_length=250, default=' - ', blank=True, verbose_name='Значение расстояния в пар-шагах')
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Shema')
    
    # Это поле хранит пары координат линии 
    # СК-42, 6-градусная зона №4 (SRID = 28404 = порядок YX)   
    location = models.LineStringField(srid=28404, verbose_name='Схема')
    
    def __str__(self):
        try:
            # Получаем объект WorldPoint [<WorldPoint: Ориентир: 2>, <WorldPoint: Ориентир: 3>] 
            # где self это WorldLine self.mypoints.all() это related_name 
            # по нему мы обращаемся к PointInLine и забираем значения поля mypoints
            # [<WorldPoint: Ориентир: 2>, <WorldPoint: Ориентир: 3>] 
            pnts = [obj_world_points.mypoints for obj_world_points in self.mypoints.all()]
            # создаем экземпляры полученного WorldPoint и забираем его имя из поля name
            pnt = [pnt.name for pnt in pnts]
            return f'Название схемы: Ориентир: {pnt[0]} - ориентир: {pnt[1]}'
        except(IndexError):
            return f'Возникла ошибка подписей линий'
    

class WorldPoint(models.Model):

    class Meta:
        verbose_name_plural = 'Схема расположения ориентиров'
        db_table = "points_model" # название модели в БД

    name = models.CharField(max_length=250, help_text='Введите название ориентира', verbose_name='Название ориентира')
    
    # Это поле хранит пары координат точки    
    location = models.PointField(srid=28404, verbose_name='Схема ориентиров')
    # SRID stands for Spatial Reference Identifier. 
    # Идентификатор системы пространственной привязки
    # Используйте целое число, представляющее код EPSG системы координат.
    # https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier

    # Переопределим название экземпляра модели в административной панели.
    def __str__(self):
        return f'Ориентир: {self.name}'
    
class PointInLine(models.Model):
    class Meta:
        verbose_name_plural = 'Таблица M:N'
        db_table = "relations_model" # название модели в БД

    mypoints = models.ForeignKey(WorldPoint, on_delete=models.CASCADE, related_name='mylines') 
    mylines = models.ForeignKey(WorldLine, on_delete=models.CASCADE, related_name='mypoints') 

# Этот код создает модель Django с двумя внешними ключами (ForeignKey). 
# Один ключ ссылается на модель WorldPoint, а другой — на модель WorldLine. 
# Атрибут on_delete=models.CASCADE указывает на то, что при удалении объекта из 
# связанной таблицы (например, WorldPoint или WorldLine) все связанные объекты PointInLine также будут 
# удалены. Параметр related_name используется для обратной ссылки на эту модель из 
# связанных моделей WorldPoint и WorldLine.

# ТАЙЛОВАЯ МОДЕЛЬ
# модель Django, которая будет отображать таблицу для хранения тайлов в базе данных
from django.contrib.gis.db import models

class Tile(models.Model):
    zoom_level = models.IntegerField() # уровень зума загруженны z5-z10
    tile_column = models.IntegerField()
    tile_row = models.IntegerField()
    tile_data = models.BinaryField()
    geom = models.PointField(srid=28404, verbose_name='Тайловая модель')  # пример геометрического поля для хранения тайлов

    class Meta:
        db_table = "tile_model"


# create point SRID=4326 это WGS84
# python manage.py shell
# >>> from geoapp.models import WorldPoint
# >>> from django.contrib.gis.geos import GEOSGeometry
# >>> pnt = GEOSGeometry('SRID=4326;POINT(954158.1 4215137.1)')
# >>> WorldPoint(name='pp', azimuth='-', pn=5.5, distance='-', location=pnt).save()
    

