import unittest
# import pytest

from Task_1 import return_filter_list, geo_logs, el 
from Task_2 import create_exeptional_ids, ids
from Task_4 import max_value, stats

# Проба пера
# --------------unittest---------------
# class Test_unittest(unittest.TestCase):

#     def test_1(self):
#         x, y = 10, 20
#         result = x + y
#         expected = 30
#         assert result == expected
    
#     def test_2(self):
#         x, y = 10, 20
#         result = summarize(x, y)
#         expected = 30
#         assert result == expected

#     def test_3(self):
#         x, y = 10, 20
#         result = summarize(x, y)
#         expected = 30
#         self.assertEqual(result, expected)

# ------------pytest------------------
# class Test_pytest:

#     @pytest.mark.parametrize(
#                                 "x, y, expected", (
#                                 (10, 20, 30),
#                                 (10, 30, 40)
#                                 )
#                             )   
    
#     def test_4(self, x, y, expected):
#         result = summarize(x, y)
#         assert result == expected

# Домашнее задание_1
# --------------unittest---------------
class TestUnittestCase(unittest.TestCase):
    '''
    Тест unittest test_main.py тестирует возвращаемые результаты функций из задач №№_1-4.
    Тест запускается под конкретную задачу, для этого ее название нужно ввести после начала тестирования
    по команде в cmd:
    python -m unittest tests/test_main.py -v для MacOS
    py -m unittest tests/test_main.py -v для Windows
    где -v - расширенная информация о результатах теста
    '''
    
    # Создание тестовой фикстуры
    def setUp(self): 
        '''
        Повторяемые действия для всех тестов в начале тестирования
        '''
        pass
    
    def tearDown(self):
        '''
        Повторяемые действия для всех тестов в конце тестирования
        '''
        pass
  
    # Создание методов теста с запуском каждого из них по условию skipIf() тестируемой задачи
    # -------ТЕСТ 1-------  
    @unittest.skipIf(number_task != 'Task_1', reason="Тест пропущен. Он для задачи №_1")
    def test_1(self):
        '''
        Тест assertMultiLineEqual.
        Элемент, по которому осуществляется фильтрация, должен совпадать с эталонным и его тип str
        Тест assertListEqual. 
        Возвращаемая функцией коллекция должна быть списком и содержать элементы, как в тестовой функции
        '''
        result_test_el = 'Россия' # Задание условия для фильтра
        result = return_filter_list(geo_logs, result_test_el)

        def return_filter_list_for_test(list_visit: list, filter_el: str) -> list:
            '''
            Тестовая функция фильтрующая входной список по заданному элементу
            filter_el - аргумент функции, по которому осуществляется фильтрация
            '''
            # ПРИМЕЧАНИЕ. Тестовая функция специально немножко изменена по сравнению с тестируемой
            for geo_logs_dict in list_visit:
                {geo_logs_dict.pop(key_) for key_, value_ in list(geo_logs_dict.items()) if value_[1] != filter_el}
                    
            return (list(filter(None, geo_logs))) #Фильтрация из списка пустых словаре

        expected = return_filter_list_for_test(geo_logs, result_test_el)
        
        # Проверяет содержимое и тип (str) второго аргумента функции 
        self.assertMultiLineEqual(
            el, result_test_el, msg='Тест не пройден. Элемент,'
            'по которому осуществляется фильтрация, не совпадает с'
            'эталонным или его тип не str'
        ) 
        # Проверяет содержимое и тип (list) данных возвращаемых функцией 
        self.assertListEqual(
            result, expected, msg='Тест не пройден. Содержимое и(или) тип данных,'
            'возвращаемых функцией не совпадают с эталонными list'
        )
         
    # -------ТЕСТ 2-------
    @unittest.skipIf(number_task != 'Task_2', reason="Тест пропущен. Он для задачи №_2")
    def test_2(self):
        '''
        Тест assertListEqual. 
        Возвращаемая функцией коллекция должна быть списком и содержать элементы, как в тестовой функции
        '''
        result = create_exeptional_ids(ids)

        def create_exeptional_ids_for_test(id_numbers: dict) -> list:
            '''
            Тестовая функция создания уникальных элементов из входного словаря
            '''
            exeptional_ids = set()
            for id_number in id_numbers:
                exeptional_ids = exeptional_ids | set(ids[id_number])
            
            return list(exeptional_ids)

        expected = create_exeptional_ids_for_test(ids)

        self.assertListEqual(
            result, expected, msg='Тест не пройден. Содержимое и(или) тип данных, '
            'возвращаемых функцией не совпадают с эталонными list'
        )
    
    # -------ТЕСТ 3-------
    @unittest.skipIf(number_task != 'Task_3', reason="Тест пропущен. Он для задачи №_3")
    def test_3(self):
        print('Для этой задачи тест не разрабатывался')

    # -------ТЕСТ 4-------
    @unittest.skipIf(number_task != 'Task_4', reason="Тест пропущен. Он для задачи №_4")
    def test_4(self):
        '''
        Тест assertMultiLineEqual. 
        Возвращаемая функцией коллекция должна быть строкой и содержать элементы, как в тестовой функции
        '''
        result = max_value(stats)

        def max_value_test(stats_dict: dict) -> str:
            '''
            Тестовая функция возвращающая максимальный рейтинг
            '''
            result = max(stats_dict, key=stats_dict.get)
        
            return result

        expected = max_value_test(stats)

        self.assertMultiLineEqual(
            result, expected, msg='Тест не пройден. Содержимое и(или) тип данных,' 
            'возвращаемых функцией не совпадают с эталонными str'
        )

if __name__ == '__main__':
    unittest.main()
    # pytest.main()
