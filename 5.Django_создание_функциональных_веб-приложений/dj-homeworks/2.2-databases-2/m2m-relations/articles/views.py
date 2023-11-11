from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    '''Обработчик'''
    template = 'articles/news.html'
    # ordering = '-published_at'
    # object_list = Article.objects.all().order_by(ordering)
    # Сортировка по дате публикации перемещена в models.Meta()
    object_list = Article.objects.all()
    context = {
        'object_list': object_list
    }

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    # ordering = '-published_at'

    return render(request, template, context)
