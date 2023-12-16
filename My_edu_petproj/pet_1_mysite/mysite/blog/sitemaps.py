# Добавление карты сайта.
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    #     Мы определили конкретно-прикладную карту сайта, унаследовав класс
    # Sitemap модуля sitemaps. Атрибуты changefreq и priority указывают частоту
    # изменения страниц постов и их релевантность на веб-сайте (максимальное
    # значение равно 1).
    
    def items(self):
        return Post.published.all()
        # Метод items() возвращает набор запросов QuerySet объектов, подлежащих
        # включению в эту карту сайта. По умолчанию Django вызывает метод get_absolute_
        # url() по каждому объекту, чтобы получить его URL-адрес.
    
    def lastmod(self, obj):
        return obj.updated
        # Метод lastmod получает каждый возвращаемый методом items() объект
        # и возвращает время последнего изменения объекта.
        # Атрибуты changefreq и priority могут быть либо методами, либо атрибута-
        # ми.

        # Мы создали карту сайта. Теперь необходимо создать для него URL-адрес.
        # Отредактируйте главный файл urls.py проекта mysite, добавив карту сайта