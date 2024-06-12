from django.contrib.gis.db import models


class ImportTrek(models.Model):

    class Meta:
        verbose_name_plural = 'Импорт точек маршрута'
        db_table = "trek_model" # название модели в БД
    name = models.CharField(max_length=250, default=' - ', blank=False, verbose_name='Название точек')
    # Это поле хранит пары координат точки    
    location = models.PointField(srid=4326, verbose_name='Местонахождение точки')
    
    # Переопределим название экземпляра модели в административной панели.
    def __str__(self):
        return f'{self.name}'


class ImportTrekLine(models.Model):

    class Meta:
        verbose_name_plural = 'Создание линии по точкам'
        db_table = "trek_line_model" # название модели в БД
    
    name = models.CharField(max_length=250, default=' - ', blank=False, verbose_name='Название участка маршрута')
    azimuth = models.CharField(max_length=250, default=' - ', blank=False, verbose_name='Значение азимута магнитного')
    pn = models.FloatField(default=0, blank=False, verbose_name='Поправка направления')
    distance = models.CharField(max_length=250, default=' - ', blank=False, verbose_name='Значение расстояния в пар-шагах')

    # Это поле хранит пары координат точек    
    location = models.LineStringField(srid=4326, verbose_name='Местонахождение маршрута')

    def __str__(self):
        try: 
            pnts = [obj_world_points.mypoints for obj_world_points in self.mypoints.all()]
            pnt = [pnt.name for pnt in pnts]
            return f'Участок маршрута: {pnt[0]} - {pnt[1]}'
        except(IndexError):
            return f'Возникла ошибка подписей линий'
    

class PointInLine(models.Model):
    class Meta:
        verbose_name_plural = 'Таблица M:N точки-линии'
        db_table = "relations_p_l_model" # название модели в БД

    mypoints = models.ForeignKey(ImportTrek, on_delete=models.CASCADE, related_name='mylines') 
    mylines = models.ForeignKey(ImportTrekLine, on_delete=models.CASCADE, related_name='mypoints') 

    
class ImportInc(models.Model):

    class Meta:
        verbose_name_plural = 'Импорт точек инцидента'
        db_table = "my_inc_model" 
        unique_together = [['name', 'location']] # Наборы полей, которые в совокупности должны быть уникальны
    
    name = models.CharField(max_length=250, default=' - ', blank=True, verbose_name='Название инцидента')
       
    location = models.PointField(srid=4326, verbose_name='Местонахождение инцидентов')
    
    def __str__(self):
        return f'{self.name}'


class Person(models.Model):

    class Meta:
        verbose_name_plural = 'Сотрудники'
        db_table = "person_model" 
    
    person_name = models.CharField(max_length=250, default=' - ', blank=True, verbose_name='Имя сотрудника')
    
    def __str__(self):
        return f'{self.person_name}'


class IncInPerson(models.Model):
    class Meta:
        verbose_name_plural = 'Таблица M:N сотрудники-инциденты'
        db_table = "relations_inc_pers_model" # название модели в БД

    incendent = models.ForeignKey(ImportInc, on_delete=models.CASCADE, related_name='person') 
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='incendent') 