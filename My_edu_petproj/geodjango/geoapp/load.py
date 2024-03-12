# Импорт shape в gdb с помощью LayerMapping
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder

# Каждый ключ в словаре world_mapping соответствует полю в модели WorldBorder. 
# Значение - это имя поля шейп-файла, из которого будут загружены данные.
# Ключом mpoly для поля геометрии является MULTIPOLYGON, 
# тип геометрии, в качестве которого GeoDjango будет импортировать поле. 
# Даже простые полигоны в шейпфайле будут автоматически преобразованы 
# в коллекции перед вставкой в базу данных. 

world_mapping = {
    "fips": "FIPS",
    "iso2": "ISO2",
    "iso3": "ISO3",
    "un": "UN",
    "name": "NAME",
    "area": "AREA",
    "pop2005": "POP2005",
    "region": "REGION",
    "subregion": "SUBREGION",
    "lon": "LON",
    "lat": "LAT",
    "mpoly": "MULTIPOLYGON",
}

# Путь к шейп-файлу не является абсолютным - другими словами, если вы переместите приложение geoapp
# (с подкаталогом data) в другое место, сценарий все равно будет работать.
world_shp = Path(__file__).resolve().parent / "data" / "TM_WORLD_BORDERS-0.3.shp"

# Ключевое слово transform установлено в False, потому что данные в шейпфайле 
# не нужно преобразовывать - они уже находятся в WGS84 (SRID=4326). 
def run(verbose=True):
    lm = LayerMapping(WorldBorder, world_shp, world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

# После этого вызовите оболочку Django из каталога проекта geodjango
# python manage.py shell
# Далее импортируем модуль load, вызываем процедуру run и наблюдаем, 
# как LayerMapping выполняет свою работу
# from geoapp import load
# load.run()

# Все это дело можно автоматизировать
# введя в cmd
# python manage.py ogrinspect geoapp/data/TM_WORLD_BORDERS-0.3.shp WorldBorder --srid=4326 --mapping --multi
# тогда на выходе мы получим 
# # This is an auto-generated Django model module created by ogrinspect.
# from django.contrib.gis.db import models


# class WorldBorder(models.Model):
#     fips = models.CharField(max_length=2)
#     iso2 = models.CharField(max_length=2)
#     iso3 = models.CharField(max_length=3)
#     un = models.IntegerField()
#     name = models.CharField(max_length=50)
#     area = models.IntegerField()
#     pop2005 = models.BigIntegerField()
#     region = models.IntegerField()
#     subregion = models.IntegerField()
#     lon = models.FloatField()
#     lat = models.FloatField()
#     geom = models.MultiPolygonField(srid=4326)


# # Auto-generated `LayerMapping` dictionary for WorldBorder model
# worldborder_mapping = {
#     'fips': 'FIPS',
#     'iso2': 'ISO2',
#     'iso3': 'ISO3',
#     'un': 'UN',
#     'name': 'NAME',
#     'area': 'AREA',
#     'pop2005': 'POP2005',
#     'region': 'REGION',
#     'subregion': 'SUBREGION',
#     'lon': 'LON',
#     'lat': 'LAT',
#     'geom': 'MULTIPOLYGON',
# }

# ПРЕОБРАЗУЕМ из бд в GEOJSON
# from geoapp.models import WorldBorder
# sm = WorldBorder.objects.get(name="San Marino")
# sm.mpoly.geojson
# '{ "type": "MultiPolygon", "coordinates": [ [ [ [ 12.415798, 43.957954 ], [ 12.450554, 43.979721 ], [ 12.453888, 43.981667 ], [ 12.4625, 43.984718 ], [ 12.471666, 43.986938 ], [ 12.492777, 43.989166 ], [ 12.505554, 43.988609 ], [ 12.509998, 43.986938 ], [ 12.510277, 43.982773 ],
# [ 12.511665, 43.943329 ], [ 12.510555, 43.939163 ], [ 12.496387, 43.923332 ], [ 12.494999, 43.914719 ], [ 12.487778, 43.90583 ], [ 12.474443, 43.897217 ], [ 12.464722, 43.895554 ], [ 12.459166, 43.896111 ], [ 12.416388, 43.904716 ], [ 12.412222, 43.906105 ], [ 12.407822, 43.913658 ], [ 12.403889, 43.926666 ], [ 12.404999, 43.948326 ], [ 12.408888,
# 43.954994 ], [ 12.415798, 43.957954 ] ] ] ] }'
# sm = WorldBorder.objects.all()
# allm = [s.mpoly.geojson for s in sm]