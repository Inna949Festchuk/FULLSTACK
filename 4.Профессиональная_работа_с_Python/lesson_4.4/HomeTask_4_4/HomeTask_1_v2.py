# 1. Доработать класс FlatIterator в коде ниже. 
# Должен получиться итератор, который принимает список списков и 
# возвращает их плоское представление, т. е. последовательность, 
# состоящую из вложенных элементов. 
# Функция test в коде ниже также должна отработать без ошибок.

# #Делаем итератор

# class FlatIterator:
#     def __init__(self, list_of_lists:list):
#         self.list_of_lists = list_of_lists
#         self.row = 0
#         self.col = 0

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.row >= len(self.list_of_lists) or self.col >= len(self.list_of_lists[self.row]):
#             raise StopIteration
#         else:
#             val = self.list_of_lists[self.row][self.col]
#             self.col += 1
#             if self.col >= len(self.list_of_lists[self.row]):
#                 self.row += 1
#                 self.col = 0
#             return val

# #Тестируем итератор (ТЕСТ ПРОЙДЕН!)			

# list_of_lists = [
#      ['a', 'b', 'c'],
#      ['d', 'e', 'f', 'h', False],
#      [1, 2, None]
#  ]

# for x in FlatIterator(list_of_lists):
#  	print(x)

# def test_1():

#     list_of_lists_1 = [
#         ['a', 'b', 'c'],
#         ['d', 'e', 'f', 'h', False],
#         [1, 2, None]
#     ]

#     for flat_iterator_item, check_item in zip(
#             FlatIterator(list_of_lists_1),
#             ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
#     ):

#         assert flat_iterator_item == check_item
	

#     assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

		
# if __name__ == '__main__':
#     test_1()


# 2. Доработать функцию flat_generator. Должен получиться генератор, 
# который принимает список списков и возвращает их плоское представление. 
# Функция test в коде ниже также должна отработать без ошибок.

# import types

# def flat_generator(list_of_lists):

#     ...
#     yield
#     ...

# # Делаем функцию-генератор (ТЕСТ ПРОЙДЕН!)

# def flat_generator(list_of_lists:list):
#    iter_object = iter(list_of_lists)
#    while True:
#        try:
#            iter_object_values = next(iter_object)
#            iter_object_enclosure = iter(iter_object_values)
#            while True:
#                try:
#                    iter_object_enclosure_values = next(iter_object_enclosure) 
#                except StopIteration:
#                    break
#                yield iter_object_enclosure_values
#        except StopIteration:
#            break
        
# # Тестируем функцию-генератор(ТЕСТ ПРОЙДЕН!)

# list_of_lists_1 = [
#     ['a', 'b', 'c'],
#     ['d', 'e', 'f', 'h', False],
#     [1, 2, None]
# ]

# for x in flat_generator(list_of_lists_1):
# 	print(x)

# import types

# def test_2():

#     list_of_lists_1 = [
#         ['a', 'b', 'c'],
#         ['d', 'e', 'f', 'h', False],
#         [1, 2, None]
#     ]

#     for flat_iterator_item, check_item in zip(
#             flat_generator(list_of_lists_1),
#             ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
#     ):

#         assert flat_iterator_item == check_item

#     assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

#     assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


# if __name__ == '__main__':
#     test_2()


# 3.* Необязательное задание. Написать итератор, 
# аналогичный итератору из задания 1, но обрабатывающий списки с 
# любым уровнем вложенности. 
# Шаблон и тест в коде ниже:

# class FlatIterator:

#     def __init__(self, list_of_list):
#         self.list_of_list = list_of_list

#     def __iter__(self):
#         ...
#         return self
    
#     def __next__(self):
#         ...
#         return item

#Делаем итератор
class FlatIterator(object):
	""" 
	*Итератор обрабатывающий списки с любым уровнем вложенности
	Возвращает плоское представление списков
	"""
	def __init__(self, nested_list: list):
		super(FlatIterator, self).__init__()
		self.nested_list = nested_list
		self.flatten_list = []
		self._flat_list(self.nested_list)

	def __iter__(self):
		self.start = 0
		self.end = len(self.flatten_list)
		return self

	def __next__(self):
		if self.start < self.end:
			self.start += 1
			return self.flatten_list[self.start-1]
		else:
			raise StopIteration

	def _flat_list(self, elem):
		if type(elem) == list:
			for e in elem:
				self._flat_list(e)
		else:
			self.flatten_list.append(elem)
			return elem

#Тестируем итератор (ТЕСТ ПРОЙДЕН!)			

# list_of_lists = [
#    [['a'], ['b', 'c']],
#    ['d', 'e', [['f'], 'h'], False],
#    [1, 2, None, [[[[['!']]]]], []]
# ]

# for x in FlatIterator(list_of_lists):
#  	print(x)

# def test_3():

#     list_of_lists_2 = [
#         [['a'], ['b', 'c']],
#         ['d', 'e', [['f'], 'h'], False],
#         [1, 2, None, [[[[['!']]]]], []]
#     ]

#     for flat_iterator_item, check_item in zip(
#             FlatIterator(list_of_lists_2),
#             ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
#     ):

#         assert flat_iterator_item == check_item

#     assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


# if __name__ == '__main__':
#     test_3()


# 4.* Необязательное задание. Написать генератор, 
# аналогичный генератору из задания 2, но обрабатывающий списки с 
# любым уровнем вложенности. Шаблон и тест в коде ниже:

# def flat_generator(list_of_list):
#     ...
#     yield
#     ...

# ----- Делаем функцию-генератор -----
# ТЕСТ БУДЕТ ПРОЙДЕН С ПРЕДУПРЕЖДЕНИЕМ ПРИ ВЕРСИИ ИНТЕРПРИТАТОРА 3.7:
#Warning (from warnings module):
#  File "D:\Фулстек\4 Профессиональный Python\4. Итераторы Генераторы\Home_Task\HomeTask_1_v2.py", line 231
#    from collections import Iterable
#DeprecationWarning: Using or importing the ABCs from 'collections'
#instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working

# Доработка Для Python 3.8.0 - 3.10.7

from collections.abc import Iterable

def flat_generator(items, ignore_types=(str, bytes)):
   for x in items:
       if isinstance(x, Iterable) and not isinstance(x, ignore_types):
           yield from flat_generator(iter(x))
       else:
           yield x

# Тестируем генератор (ТЕСТ ПРОЙДЕН!)	

list_of_lists_2 = [
       [['a'], ['b', 'c']],
       ['d', 'e', [['f'], 'h'], False],
       [1, 2, None, [[[[['!']]]]], []]
]

for x in flat_generator(list_of_lists_2):
	print(x)

import types

def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_4()

##Примечание к необязательному заданию № 4
##Задача превращения вложенной последовательности, в один плоский
##список значений решается с помощью рекурсивного генератора
##с инструкцией yield from (Python.Книга рецептов. Дэвид Бизли) стр.147.

# from collections import Iterable

# def flatten(items, ignore_types=(str, bytes)):
#    for x in items:
#        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
#            yield from flatten(x)
#        else:
#            yield x
# items = ['Dave', 'Paula', ['a', 'b', 'c'], ['d', 'e', 'f', 'h', False], [1, 2, None]]

# for x in flatten(items):
#    print(x)
    
##В этой программе isinstance(x, Iterable) просто проверяет, является ли элемент
##итерируемым объектом. Если это так, то yield from используется в качестве некой
##подпрограммы, чтобы выдать все его значения. Конечный результат – одна по-
##следовательность без вложенности.
##Дополнительный аргумент ignore_types и проверка not isinstance(x, ignore_types)
##нужны для предотвращения определения строк и байтов как итерируемых после-
##довательностей, разбиения их на отдельные символы. Это позволяет вложенным
##спискам строк работать так, как большинство людей этого и ожидает:
##>>> items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
##>>> for x in flatten(items):
##... print(x)
##...
##Dave
##Paula
##Thomas
##Lewis
##>>>
