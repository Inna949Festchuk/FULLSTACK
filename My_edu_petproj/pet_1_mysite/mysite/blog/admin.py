from django.contrib import admin
# Импорт моделей (регистрация на сайте администрирования)
from .models import Post, Comment # Добавление постов и комментариев на сайт администрирования

# В cmd создаем суперпользователя
# python manage.py createsuperuser

# Register your models here.

# Адаптация внешнего вида моделей
# под конкретно-прикладную задачу
@admin.register(Post) # Регистрируем модель в админке
# Декоратор
# @admin.register() выполняет ту же функцию, что и функция admin.site.register()
class PostAdmin(admin.ModelAdmin):
    #     Мы сообщаем сайту администрирования, что модель зарегистрирована на
    # сайте с использованием конкретно-прикладного класса, который наследует
    # от ModelAdmin. В этот класс можно вставлять информацию о том, как показы-
    # вать модель на сайте и как с ней взаимодействовать.
    
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    #     list_display позволяет задавать поля модели, которые вы хотите
    # показывать на странице списка объектов администрирования
    
    list_filter = ['status', 'created', 'publish', 'author']
    #     Теперь страница
    # списка содержит правую боковую панель, которая позволяет фильтровать
    # результаты по полям, включенным в атрибут list_filter.
    
    search_fields = ['title', 'body']
    #     На странице появилась строка поиска. Это вызвано тем, что мы опреде-
    # лили список полей, по которым можно выполнять поиск, используя атрибут
    # search_fields
    
    prepopulated_fields = {'slug': ('title',)}
    # Далее кликните по ссылке ADD POST (Добавить пост). Здесь вы тоже заме-
    # тите некоторые изменения. При вводе заголовка нового поста поле slug запол-
    # няется автоматически. Вы сообщили Django, что нужно предзаполнять поле
    # slug данными, вводимыми в поле title, используя атрибут prepopulated_fields:

    raw_id_fields = ['author']
    #     Кроме того, теперь поле author отображается поисковым виджетом, кото-
    # рый будет более приемлемым, чем выбор из выпадающего списка, когда у вас
    # тысячи пользователей. Это достигается с помощью
    # атрибута raw_id_fields

    date_hierarchy = 'publish'
    #     Чуть ниже строки поиска на странице администрирования в браузере находятся навигационные ссылки
    # для навигации по иерархии дат; это определено атрибутом date_hierarchy
    
    ordering = ['status', 'publish']
    #     Вы также видите, что по умолчанию посты упорядочены по столбцам STATUS
    # (Статус) и PUBLISH (Опубликован). С помощью
    # атрибута ordering были
    # заданы критерии сортировки, которые будут использоваться по умолчанию.

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Добавление комментариев на сайт администрирования

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active'] # поля для заполнения
    list_filter = ['active', 'created', 'updated'] # поля фильтрации
    search_fields = ['name', 'email', 'body'] # поля поиска

    # Создание форм из моделей
    # Далее необходимо скомпоновать форму, позволяющую пользователям ком-
    # ментировать посты блога. Напомним, что в Django есть два базовых класса,
    # которые можно использовать для создания форм: Form и ModelForm. Мы ис-
    # пользовали класс Form, чтобы предоставлять пользователям возможность
    # делиться постами по электронной почте. Теперь мы будем использовать
    # ModelForm, чтобы воспользоваться преимуществами существующей модели
    # Comment и компоновать для нее форму динамически.
    # Отредактируйте файл forms.py приложения blog, добавив следующие далее
    # строки...