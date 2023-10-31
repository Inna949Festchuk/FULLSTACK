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
    # Свяжем модель с моделью Car по полю car(FK), тип связи 1:M
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='owners')
    # где Car-модель; 
    # on_delete=models.CASCADE стандартное поведение записи о человеке 
    # при удалении машины из БД (каскадное удаление)
    # related_name='owners' - т.н. обратное слово, связи 1:М 
    # говорит кто из персон является владельцем того или иного авто

# ---------------------------------------------------------------
# ORM M:M
# ---------------------------------------------------------------

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=50)

# Создаем сязь M:M
class Order(models.Model):
    produsts = models.ManyToManyField(Product, related_name='orders') # orders позволит из продукта достучаться до заказа

# Создаем промежуточную модель
class OrderPositions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions') # positions позволит из продукта достучаться до его позиции
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='positions') # positions позволит из закаа достучаться до его позиции
    # позволит указать сколько единиц товара в этом заказе
    quantity = models.IntegerField()