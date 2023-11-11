from django.db import models


class Article(models.Model):
    '''Модель статей'''
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']
        indexes = [models.Index(fields=['-published_at']), ]

    def __str__(self):
        return self.title
    

class Tags(models.Model):
    '''Модель тегов'''
    name = models.CharField(max_length=30, verbose_name='Раздел')
    # Связь m2m модели Article с моделью Tags будет осуществляться через дополнительную модель ArticleTags,
    # на что указывает параметр through
    articles = models.ManyToManyField(Article, through='TagsArticle')

    def __str__(self):
        return self.name


class TagsArticle(models.Model):
    '''Модель взамен m2m'''
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False) # Поле указания основного тега
    
    def __str__(self):
        return f'{self.article.title} - {self.tag.name}'
