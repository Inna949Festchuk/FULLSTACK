from functools import wraps


def trace_decorator(some_function):
    @wraps(some_function)  # wraps подменяет метаданные функции
    def new_function(*args, **kwargs):
        print(f'Вызываем {some_function.__name__} c аргументами {args} и {kwargs}')
        result = some_function(*args, **kwargs)
        print(f'Вернули результат {result}')
        return result

    return new_function


@trace_decorator
def hello_world():
    return 'Hello World'
