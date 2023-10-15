from django.db import models

class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=255, verbose_name='Марка')
    image = models.URLField(verbose_name='Внешний вид')
    price = models.IntegerField(verbose_name='Цена')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата изготовления')
    lte_exists = models.BooleanField(verbose_name='Наличие товара')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return f'{self.name}, {self.price}, {self.release_date}'