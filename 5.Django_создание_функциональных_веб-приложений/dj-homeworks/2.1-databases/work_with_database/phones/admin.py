from django.contrib import admin
from .models import Phone


@admin.register(Phone)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'price', 'release_date', 'lte_exists', 'slug']
    prepopulated_fields = {'slug': ('name',)} # автозаполнение слага в админке по имени


