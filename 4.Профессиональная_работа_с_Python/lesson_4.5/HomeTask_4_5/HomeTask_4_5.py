from functools import wraps
import datetime
import os

# ЗАДАНИЕ_№1

def logger(old_function):
    '''
    декоратор - логгер. Записывает в файл дату и время вызова функции,
    имя функции, аргументы, с которыми вызвалась и возвращаемое значение.
    Входной параметр – старая функция
    '''
    
    def new_function(*args, **kwargs):

        # БЛОК ДО ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
        now = datetime.datetime.now()
        log = ''
        log += f"{'Время вызова функции: ' + str(now):=^100}\n"
            
        # ВЫЗОВ ИСХОДНОЙ ФУНКЦИИ
        result = old_function(*args, **kwargs)
        log += f'Имя вызванной функции: {old_function.__name__}\n'
        log += f'Аргументы вызванной функции: {args} и {kwargs}\n'
        log += f'Значение, возвращаемое функцией {result}\n'

        # # БЛОК ПОСЛЕ ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # самонастраивающийся путь
        with open('main.log', 'a+', encoding='utf-8') as f:
            f.write(log)

            return result
        
    return new_function

# @logger
# def my_function(*args, **kwargs): # ИСХОДНАЯ (СТАРАЯ, СУЩЕСТВУЮЩАЯ) Ф-Я
#     return list(zip(args, kwargs))

# # Вызов функции с аргументами
# my_function("hello", 42, arg=3)


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

# # ЗАДАНИЕ_№2

def logger(path):
    '''
    декоратор - логгер. Записывает в файл дату и время вызова функции,
    имя функции, аргументы, с которыми вызвалась и возвращаемое значение.
    Входной параметр – путь к логам
    '''
    
    def _logger(old_function):
        
        @wraps(old_function)
        def new_function(*args, **kwargs):

            # БЛОК ДО ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
            now = datetime.datetime.now()
            log = ''
            log += f"{'Время вызова функции: ' + str(now):=^100}\n"
            
            # ВЫЗОВ ИСХОДНОЙ ФУНКЦИИ
            result = old_function(*args, **kwargs)
            log += f'Имя вызванной функции: {old_function.__name__}\n'
            log += f'Аргументы вызванной функции: {args} и {kwargs}\n'
            log += f'Значение, возвращаемое функцией {result}\n'

            # # БЛОК ПОСЛЕ ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
            os.chdir(os.path.dirname(os.path.abspath(__file__))) # самонастраивающийся путь
            with open(path, 'a+', encoding='utf-8') as f:
                f.write(log)

            return result
        
        return new_function
    
    return _logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()


# ЗАДАНИЕ_№3 Применить написанный логгер к приложению из любого предыдущего д/з.


def logger(path):
    '''
    декоратор - логгер. Записывает в файл дату и время вызова функции,
    имя функции, аргументы, с которыми вызвалась и возвращаемое значение.
    Входной параметр – путь к логам
    '''
    
    def _logger(old_function):
        
        @wraps(old_function)
        def new_function(*args, **kwargs):

            # БЛОК ДО ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
            now = datetime.datetime.now()
            log = ''
            log += f"{'Время вызова функции: ' + str(now):=^100}\n"
            
            # ВЫЗОВ ИСХОДНОЙ ФУНКЦИИ
            result = old_function(*args, **kwargs)
            log += f'Имя вызванной функции: {old_function.__name__}\n'
            log += f'Аргументы вызванной функции: {args} и {kwargs}\n'
            log += f'Значение, возвращаемое функцией {result}\n'

            # # БЛОК ПОСЛЕ ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
            os.chdir(os.path.dirname(os.path.abspath(__file__))) # самонастраивающийся путь
            with open(path, 'a+', encoding='utf-8') as f:
                f.write(log)

            return result
        
        return new_function
    
    return _logger

def test_3():

    paths = ('log_foo_1.log', 
            )

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def call(weekday, days):
            '''Функция отрисовки календаря 
            Параметы:  days - количество дней в месяце 
            weekday - название дня недели, на который приходится первое число месяца, записанное на английском языке.
            Первая неделя дополняется значениями "..", если это требуется. Однозначные числа записываются в формате ".число"
            '''
            if weekday == 'Monday':
                start = 1
            elif weekday == 'Tuesday':
                start = 0 
            elif weekday == 'Wednesday':
                start = -1 
            elif weekday == 'Thursday':
                start = -2 
            elif weekday == 'Friday':
                start = -3 
            elif weekday == 'Saturday':
                start = -4 
            elif weekday == 'Sunday':
                start = -5 
        
            out = ['',]
            i = 0
            for k in range(start, days + 1):
                if k <= 0:
                    out.append('..')
                elif 0 < k < 10:
                    out.append(f'.{k}')
                else:
                    out.append(k)
                i += 1
                if i % 7 == 0:
                    out.append('\n')

            return out
   
        calendar = call('Thursday', 30)
        print(*calendar)

if __name__ == '__main__':
    test_3()
