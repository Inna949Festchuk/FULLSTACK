"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap # Добавление карты сайта
from blog.sitemaps import PostSitemap # Добавление карты сайта

# Добавление карты сайта
sitemaps = {
        'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    #     Далее необходимо вставить шаблоны URL-адресов приложения blog в глав-
    # ные шаблоны URL-адресов проекта.
    #     Новый шаблон URL-адреса, определенный с помощью
    # функции include, ссылается на шаблоны URL-адресов, определенные в приложении blog, что-
    # бы они были включены в рамки пути blog/.
    path('blog/', include('blog.urls', namespace='blog')),
    #     Позже можно будет легко ссылаться
    # на URL-запросы блога, используя именное пространство, за которым следует
    # двоеточие, и имя URL-запроса, например blog:post_list и blog:post_detail.
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
                            name='django.contrib.sitemaps.views.sitemap') # Добавление карты сайта
    #     Пройдите по URL-адресу http://127.0.0.1:8000/sitemap.xml в своем браузе-
    # ре. Вы увидите результат в формате XML, включающий все опубликованные
    # посты
]

# Создание шаблонов представлений templates
# templates/
#     blog/
#         base.html
#     post/
#         list.html
#         detail.html
# Приведенная выше структура будет файловой структурой ваших шабло-
# нов. Файл base.html будет включать в себя главную HTML-структуру веб-сайта
# и разделит контент на главную область содержимого и боковую панель. Фай-
# лы list.html и detail.html будут наследовать от файла base.html, чтобы про-
# рисовывать представления соответственно списка постов блога и детальной
# информации о посте.
# Django обладает мощным языком шаблонов, который позволяет указывать
# внешний вид отображения данных. Он основан на шаблонных тегах, шаблон-
# ных переменных и шаблонных фильтрах:
    # •• шаблонные теги управляют прорисовкой шаблона и выглядят как {% tag %};
    # •• шаблонные переменные заменяются значениями при прорисовке шаблона
    # и выглядят как {{ variable }};
    # •• шаблонные фильтры позволяют видоизменять отображаемые перемен-
    # ные и выглядят как {{ variable|filter }}.