

def template(old_function):
    """простой декоратор"""

    def new_function(*args, **kwargs):
        ...  # код до вызова исходной функции
        result = old_function(*args, **kwargs)
        ...  # код после вызова исходной функции
        return result

    return new_function


@template
def hello_world():
    return 'Hello World'
