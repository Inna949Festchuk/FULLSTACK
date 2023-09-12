from django.db import models

# Create your models here.

# БД о машинах и их владельцах
# Опишем модель, которая будет храниться в БД
class Car(models.Model):
    # Создаем атрибуты класса (они же поля будующей таблицы БД)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.brand}, {self.model}: {self.color}'


class Person(models.Model):
    name = models.CharField(max_length=50)
    # Свяжем модель с моделью Car по полю car(FK)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='owners')
    # где Car-модель; 
    # on_delete=models.CASCADE стандартное поведение записи о человеке 
    # при удалении машины из БД (каскадное удаление)
    # related_name='owners' связь 1:М (т.н. обратное слово)
    # т.е. показывает сколько владельцев у данного авто