from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tags, TagsArticle


# class TagsArticleInlineFormset(BaseInlineFormSet):
#     '''Проверка на единство основного Тега'''
#     def clean(self):
#         super().clean() # вызываем базовый код переопределяемого метода
#         # Проверяем словари форм по ключу is_main и если ключ = True суммируем единицы,
#         # если результирующая сумма единиц больше 1 выдать предупреждение ValidationError 
#         main_scopes_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))
#         # В form.cleaned_data это словарь с проверяемыми данными
#         if main_scopes_count != 1:
#             raise ValidationError("Основной раздел может быть только один")

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
    model = TagsArticle # Модель, в которую будет встроена инлайнмодель
    formset = TagsArticleInlineFormset # Проверка на единство основного Тега
    extra = 1 # Число строк встраиваемой модели


# Регистрация модели Статьи в админке
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title', 
        'published_at',
    ]
    inlines = [
        TagsArticleInline,
    ]


# Регистрация модели Теги в админке
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'name',
    ]