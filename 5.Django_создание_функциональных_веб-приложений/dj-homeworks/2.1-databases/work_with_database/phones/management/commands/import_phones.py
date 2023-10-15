import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.template.defaultfilters import slugify # фильтр джанго


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--create',
            action='store_true',
            default=False,
            help='Заполнение базы данными'
        )
        
    def handle(self, *args, **options):
        # Phone.objects.filter(all).delete()

        if options['create'] or options['c']:
            with open('phones.csv', 'r') as file:
                phones = list(csv.DictReader(file, delimiter=';'))

            for phone in phones:
                # TODO: Добавьте сохранение модели
                Phone.objects.create(
                    name=phone.get('name'), 
                    image=phone.get('image'), 
                    price=phone.get('price'),
                    release_date=phone.get('release_date'),
                    lte_exists=phone.get('lte_exists'),
                    slug=slugify(phone.get('name')),
                )

        else:
            print('Для наполнения базы данных введите python manage.py import_phones -c')

# {'id': '1', 
#  'name': 'Samsung Galaxy Edge 2', 
#  'image': 'https://avatars.mds.yandex.net/get-mpic/364668/img_id5636027222104023144.jpeg/orig', 
#  'price': '73000', 
#  'release_date': '2016-12-12', 
#  'lte_exists': 'True'}

# Можно еще одним вариантом сделать, это метод .save() просто 
# переопределить в моделе, чтобы слаг заполнялся автоматически
#     def save(self, *args, **kwargs):  # new
#         if not self.slug:
#             self.slug = slugify(self.name)
#         return super().save(*args, **kwargs)

# super позволяет изменить дополнить метод save, 
# не ковыряя его под копотом

# А далее
# Phone(name=phone['name'],
# price=phone['price'], 
# image=phone['image'], 
# release_date=phone['release_date'], 
# lte_exists=phone['lte_exists']).save()

# Можно посмотреть здесь 
# https://qna.habr.com/q/307406
# https://proghunter.ru/articles/django-base-2023-automatic-slug-generation-cyrillic-handling-in-django-9