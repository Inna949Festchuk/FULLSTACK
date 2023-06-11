##def trace(old_function):
##
##    def new_function(*args, **kwargs):
##
##        # БЛОК ДО ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
##        print(f'Вызвана ф-я {old_function.__name__} с аргументами {args} и {kwargs}')
##
##        # ВЫЗОВ ИСХОДНОЙ ФУНКЦИИ
##        result = old_function(*args, **kwargs)
##
##        # БЛОК ПОСЛЕ ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
##        print(f'Возвращено {result}')
##
##        return result
##
##    return new_function
##
##@trace
##def multiply(a, b): # ИСХОДНАЯ (СТАРАЯ, СУЩЕСТВУЮЩАЯ) Ф-Я
##    return a * b
##
### ПРОВЕРЯЕМ
##multiply(2, 4)
###>>>Вызвана ф-я multiply с аргументами (2, 4) и {}
###>>>Возвращено 8

#КЭШИРОВАНИЕ-сохранение функции,
#вызываемой повторно с темиже аргументами, в словаре
#для повторного применения

import datetime

def cached(max_size): # ФАБРИКА
    def _cached(old_function):

        cache = {}

        def new_function(*args, **kwargs):
            key = f'{args}_{kwargs}'

            if key in cache:
                return cache[key]

            if len(cache) >= max_size:
                cache.popitem() # очистка кеша
                
            result = old_function(*args, **kwargs)
            cache[key] = result
            return result

        return new_function
    return _cached

@cached(max_size=5)
def sum(a, b, c):
    return a + b * c

##>>> sum(3, 4, 10)
##43

start = datetime.datetime.now()
print(sum(3, 4, 10))
end = datetime.datetime.now()
print(end - start)

start = datetime.datetime.now()
print(sum(3, 4, 10))
end = datetime.datetime.now()
print(end - start)
