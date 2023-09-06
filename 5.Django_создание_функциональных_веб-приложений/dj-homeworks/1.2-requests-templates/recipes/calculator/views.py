from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def index(request):
    # context = {'dat': (', ').join(list(DATA.keys()))}
    context = {list(DATA.keys())[0]: 'omlet',
               'pasta': 'pasta', 
               'buter': 'buter'}
    return render (request, 'calculator/link.html', context)

# ВАРИАНТ_№1 для url
# http://127.0.0.1:8000/omlet/?servings=4

def prepare(request, recipe):
    servings = request.GET.get('servings', 1)
    context = {
        'dish':recipe,
        'servings':servings,
        'recipe':{
            k:v*int(servings) for k, v in DATA.get(recipe, {}).items()
        }
    }
    return render (request, 'calculator/index.html', context)

# ВАРИАНТ_№2 для url
# http://127.0.0.1:8000/prepare/?recipe=omlet&servings=4

# def prepare(request):
#     recipe = request.GET.get('recipe')
#     servings = request.GET.get('servings', 1)
#     context = {'recipe':{k:v*int(servings) for k, v in DATA.get(recipe, {}).items()}}
#     # return render (request, 'calculator/index.html', context)
#     return HttpResponse(f'Это ваши рецепты {context}')
