import datetime
import os

def logger(old_function):
    
    def new_function(*args, **kwargs):

        # БЛОК ДО ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
        now = datetime.datetime.now()
        log = ''
        log += f"{'Время вызова функции: ' + str(now):=^100}\n"
            
        # ВЫЗОВ ИСХОДНОЙ ФУНКЦИИ
        
        result = old_function(*args, **kwargs)
        log += f'Имя вызванной функции: {old_function.__name__}\n'
        log += f'Аргументы вызванной функции: {args} и {kwargs}\n'
        log += f'Значение, возвращаемое функцией: {result}\n'

        # # БЛОК ПОСЛЕ ВЫЗОВА ИСХОДНОЙ ФУНКЦИИ
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # самонастраивающийся путь
        with open('logfile.log', 'a+', encoding='utf-8') as f:
            f.write(log)

            return result
        
    return new_function