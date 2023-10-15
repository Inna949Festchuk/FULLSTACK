from .models import Phone
from django.shortcuts import render, redirect
from django.core.paginator import Paginator # Добавляем пагинацию


def index(request):
    return redirect('catalog') #  редирект на каталог телефонов по имени его пути 'catalog'


def show_catalog(request):
    phones = Phone.objects.all()
    template = 'catalog.html'

    # сортировка
    sort_param = request.GET.get('sort') # Извлекаем из запроса параметр sort
    if sort_param == 'name':
        phones = phones.order_by('name') # Сортируем по полям name, price, -price(в обратном порядке)
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')
    
    # Постраничная разбивка с 2 постами на страницу 
    paginator = Paginator(phones, 2)
    page_number = request.GET.get('page', 1)
    phones = paginator.page(page_number)
    # также добавляем шаблон 'pagination.html'
    
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone':phone}
    return render(request, template, context)


