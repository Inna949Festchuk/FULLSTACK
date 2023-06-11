#Задача_4_Написать скрипт возвращающий канал с максимальным рейтингом
stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}

from tests.logger import logger

@logger
def max_value(stats_dict: dict) -> str:
    res_key = []
    res_val = []
    for key, val in stats_dict.items():
        res_key.append(key)
        res_val.append(val)
        s = max(list(zip(res_val, res_key)))
    return s[1]

if __name__ == '__main__':
    print(max_value(stats))

