# Задача_№1
# Дан список с визитами по городам и странам. Напишите код, 
# который возвращает отфильтрованный список geo_logs, содержащий только визиты из России.
geo_logs = [
    {'visit1': ['Москва', 'Россия']},
    {'visit2': ['Дели', 'Индия']},
    {'visit3': ['Владимир', 'Россия']},
    {'visit4': ['Лиссабон', 'Португалия']},
    {'visit5': ['Париж', 'Франция']},
    {'visit6': ['Лиссабон', 'Португалия']},
    {'visit7': ['Тула', 'Россия']},
    {'visit8': ['Тула', 'Россия']},
    {'visit9': ['Курск', 'Россия']},
    {'visit10': ['Архангельск', 'Россия']}
]

el = 'Россия'

from tests.logger import logger

@logger
def return_filter_list(list_visit: list, filter_el: str) -> list:
  for geo_logs_dict in geo_logs:
    for key_, value_ in list(geo_logs_dict.items()):
      if value_[1] != filter_el:
        geo_logs_dict.pop(key_) #Удаление содержимого словаря по ключу
  return (list(filter(None, geo_logs))) #Фильтрация из списка пустых словарей 

if __name__ == '__main__':
    print(return_filter_list(geo_logs, el))