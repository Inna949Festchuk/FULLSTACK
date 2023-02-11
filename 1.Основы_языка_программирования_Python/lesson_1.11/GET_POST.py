# Установка библиотеки в терминале  pip install requests

from pprint import pprint
import requests

# TOKEN = ""

# def test_request():
#     
#     url = "https://bootssizes/get"
#     params = {"model": "nike123"}
#     headers = {"Autoriszation": "secret - token - 123"}
#     response = requests.get(url, params=params, headers=headers, timeout=5)
#     pprint(response)

# # точка входа (мы говорим интепритатору питона откуда начинать вход
# # от сюда начинается выполнение функции)
# if __name__ == '__main__':
#     test_request()

TOKEN = ""

def test_request():
    
    url = "http://192.168.0.105/test.php" # Стучимся на малинку
    
    response = requests.get(url)
    
    if response.status_code == 200: # Так можно сформировать обработчики ошибок (котиков)
        print('OK**********')
    else:
        print('NO**********')
    # Узнаем что же вернулось в запросе
    # например контент
    # print(response.content)
    # text
    pprint(response.text)
    # json
    # pprint(response.json())
    # Можно посмотреть заголовок
    # pprint(response.headers)
    # Проверка Content-Type что пришло в ответе (например 'text/html; charset=utf-8')
    # if response.headers["Content-Type"] == "text/html; charset=utf-8":
    #     pprint(response.text)

    # ПЕРЕДАЧА ПАРАМЕТРОВ. Параметры передаются в виде словаря
    # params = {'key':'value'}
    # headers = {'key':'value'}
    # response = requests.get(url, headers=headers, params=params, timeout=5) 
    # время ожидания для выполнения запроса, если
    # за это время запрос не будет выполнен он будет
    # прерван
    # Это может быть не только GET, но и POST запрос, или иной другой
    # params = {'key':'value'}
    # headers = {'key':'value'}
    # data = {'key':'value'} # То что мы хотим передать запросом POST 
    # response = requests.get(url, headers=headers, params=params, timeout=5, data=data, json=data) 

    # pprint(response)

if __name__ == '__main__':
    test_request()