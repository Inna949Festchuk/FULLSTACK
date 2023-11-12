from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tags, TagsArticle


class TagsArticleInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_counter = 0
        for form in self.forms:
            # form.cleaned_data это словарь с проверяемыми данными
            if form.cleaned_data.get('is_main'):
                is_main_counter += 1
            # ValidationError - обработчик исключений
        if is_main_counter > 1:
            raise ValidationError('Основной раздел может быть только один')
        return super().clean() 


class TagsArticleInline(admin.TabularInline):
    '''Модель инлайн'''
    model = TagsArticle # Модель, которaя будет встраиваться
    formset = TagsArticleInlineFormset # Проверка на единство основного Тега
    extra = 1 # Число строк встраиваемой модели


# Регистрация модели Теги в админке
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'name',
    ]
    search_fields = [
        'name',
    ]
    list_display_links = [
        'name',
    ]
    list_per_page = 5  


# Регистрация модели Статьи в админке
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title',
        'published_at',
    ]
    # Фильтрация статей по дате публикации и по тегу
    list_filter = [
        'published_at',
        'scopes__tag__name',
    ]

    # Поиск статьи для изменения
    search_fields = [
        'title',
    ]
    # Ссылка на поле title в админке
    list_display_links = [
        'title',
    ]
    # Пагинация в админке 2 страницы
    list_per_page = 2

    # Интеграция инлайнмодели на страницу редактирования статей
    inlines = [
        TagsArticleInline,
    ]








    