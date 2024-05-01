import requests

# Создаем точки
def i_created_point(name:str, Y:float, X:float):
    url = "http://127.0.0.1:8000/api/create_point/"
    name = name
    location = f"SRID=28404;POINT({Y} {X})"
    response = requests.post(url, data={"name": name, "location": location})
    
# Рассчет схемы
def i_created_line(Pn:float=0):
    url = "http://127.0.0.1:8000/api/create_line/"
    Pn = Pn
    response = requests.post(url, data={"pn": Pn})

# Показ точки
def i_show_point():
    url = "http://127.0.0.1:8000/api/show_point/"
    response = requests.get(url)
    print(response.json())

# Показ линии
def i_show_line():
    url = "http://127.0.0.1:8000/api/show_line/"
    response = requests.get(url)
    print(response.json())

def main():
    
    while(True):
        print('\nВвведите команду: '+
              '\np - добавить тоочку,'+
              '\ns - рассчитать схему,'+
              '\nsp - показать точки,'+
              '\nsl - показать линии,'+
              '\nq - выход')
        command = input().lower()
        if command == 'p':
           i_created_point(input('Введите имя точки: '), input('Введите Y: '), input('Введите X: '))
        elif command == 's':
           i_created_line(input('Введите поправку направления: '))
        elif command == 'sp':
           i_show_point()
        elif command == 'sl':
           i_show_line()
        elif command == 'q':
           break
        else:
            print('введите правильную команду или q')
main()  
