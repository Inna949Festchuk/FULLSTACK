from django.urls import path
# from articles.views import articles_list
from . import views # Второй способ

app_name = 'articles'

urlpatterns = [
    path('', views.articles_list, name='articles'),
]
