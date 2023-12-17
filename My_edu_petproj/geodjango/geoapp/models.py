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
        # return self.name

# class WorldLine(models.Model):
#     name = models.CharField(max_length=50)
#     lon = models.FloatField()
#     lat = models.FloatField()

#     # GeoDjango-specific: a geometry field (MultiLineString)
#     mline = models.MultiLineStringField()

#     # Returns the string representation of the model.
#     def __str__(self):
#         return self.name

class WorldPoint(models.Model):
    name = models.CharField(max_length=250, help_text='Название ориентира', verbose_name='Название ориентира')
    # x = models.CharField(max_length=250, default=' - ', blank=True, help_text='Значение азимута магнитного', verbose_name='Значение азимута магнитного')
    # y = models.CharField(max_length=250, default=' - ', blank=True, help_text='Значение расстояния в пар-шагах', verbose_name='Значение расстояния в пар-шагах')
    x = models.CharField(max_length=250, help_text='Значение азимута магнитного', verbose_name='Значение азимута магнитного')
    y = models.CharField(max_length=250, help_text='Значение расстояния в пар-шагах', verbose_name='Значение расстояния в пар-шагах')

    # Это поле хранит пары координат точки    
    location = models.PointField()

    # Переопределим название экземпляра модели в административной панели.
    def __str__(self):
        return self.name

# create point SRID=4326 это WGS84
# python manage.py shell
# >>> from geoapp.models import WorldPoint
# >>> from django.contrib.gis.geos import GEOSGeometry
# >>> pnt = GEOSGeometry('SRID=4326;POINT(954158.1 4215137.1)')
# >>> WorldPoint(name='pp', x=4215137.1, y=954158.1, location=pnt).save()