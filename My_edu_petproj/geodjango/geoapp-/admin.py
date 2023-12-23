# from django.contrib import admin
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

from django.contrib.gis import admin
from .models import (
    # WorldBorder, 
    WorldPoint,
    WorldLine,
)

# admin.site.register(WorldBorder, admin.ModelAdmin)

# @admin.register(WorldBorder)
# class WorldBorderAdmin(admin.OSMGeoAdmin):
#     list_display = ('name', 'lon', 'lat')

# admin.site.register(WorldPoint, admin.ModelAdmin)

@admin.register(WorldPoint)
class WorldPointAdmin(admin.OSMGeoAdmin):
    # начиная с django v.4 использовать GISModelAdmin
    list_display = ('name', )

@admin.register(WorldLine)
class WorldPointAdmin(admin.OSMGeoAdmin):
    # начиная с django v.4 использовать GISModelAdmin
    list_display = ('azimuth', 'pn', 'distance', )