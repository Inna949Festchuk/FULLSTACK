import requests
from tqdm import tqdm

def ingenious(person1='Hulk', person2='Captain America', person3='A-Bomb'):
    # Формируем GET запрос к серверу с применением 
    # стандартного программного интерфейса API
    response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
    di= {}
    i = 0 # Итератор персонажей 
    # tqdm() - функция для создания статус-бара
    for i in tqdm(range(len(response.json()))):
        nm = response.json()[i]['name']
        if nm == person1 or nm == person2 or nm == person3:
            intelligences = response.json()[i]['powerstats']['intelligence']
            di[nm] = intelligences
        i += 1         
    # Поиск в словаре ключа с максимальным значением интеллекта
    max_val = max(di.values())
    final_dict = {k:v for k, v in di.items() if v == max_val} 

    # Форматирование выходной строки
    strings = []
    for key, item in final_dict.items():
        strings.append('Самый умный: {}. \n' 
                       'Уровень его интеллекта равен: {}.'.format(key, item))
    result = ', '.join(strings)

    return result

if __name__ == '__main__':
    print(ingenious('','','Thanos'))





    
    

