# Выведите на экран все уникальные гео-ID из значений словаря ids.
# Т.е. список вида [213, 15, 54, 119, 98, 35]

ids = {'user1':[213, 213, 213, 15, 213],
       'user2':[54, 54, 119, 119, 119],
       'user3':[213, 98, 98, 35],
       'user8':[1, 5, 9, 15]}

from tests.logger import logger

@logger
def create_exeptional_ids(id_numbers: dict) -> list:
    '''Функция создания уникальных id
    '''
    exeptional_ids = set()
    for id_number in id_numbers:
        exeptional_ids = exeptional_ids | set(ids[id_number])
    return list(exeptional_ids)

if __name__ == '__main__':
    print(create_exeptional_ids(ids))
    

