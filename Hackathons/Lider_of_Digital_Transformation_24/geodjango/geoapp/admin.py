# from django.contrib import admin
from django.contrib.gis import admin
from .models import (
    ImportTrek,
    ImportTrekLine,
    ImportInc,
    Person,
    IncInPerson,
)


# Регистрируем модель точек в админпанели GeoDjango
@admin.register(ImportTrek)
class ImportTrekAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('name', 'location', )

@admin.register(ImportTrekLine)
class ImportTrekLineAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('name', 'azimuth', 'pn', 'distance', 'location', )

@admin.register(ImportInc)
class ImportIncAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('name', 'location', )

@admin.register(Person)
class PersonAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('person_name', )


@admin.register(IncInPerson)
class IncInPersonAdmin(admin.GISModelAdmin):
    # начиная с django v.4 использовать GISModelAdmin, ниже - OSMGeoAdmin
    list_display = ('incendent', 'person', )
