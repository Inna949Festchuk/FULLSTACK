from django.db import models

class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=255, verbose_name='Марка')
    image = models.URLField(verbose_name='ДВнешний вид')
    price = models.IntegerField(verbose_name='Цена')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата изготовления')
    lte_exists = models.BooleanField(verbose_name='Наличие товара')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    
    def __str__(self):
        return f'{self.name}, {self.price}, {self.release_date}'
    
    pass

# # на пайтоне сделать поле в модели джанго содержащее ссылки на картинку которая хранится на другом сайте
# # В модели Django вы можете использовать поле типа URLField для хранения ссылок на картинки, которые хранятся на другом сайте. Вот пример:
# from django.db import models
# class MyModel(models.Model):
#     image_url = models.URLField()
# # В этом примере image_url является полем модели, которое будет содержать ссылку на картинку. При создании объекта MyModel, вы можете передать URL-адрес изображения в поле image_url. Например:
# my_object = MyModel(image_url='https://www.example.com/image.jpg')
# my_object.save()
# # Затем вы можете получить ссылку на картинку и использовать ее в вашем представлении или шаблоне Django для отображения изображения.