##Делаем итератор списка без вложений

# class ClassIterator:
    
#     def __init__(self, list_of_list):
#         self.list_of_list = list_of_list

#     def __iter__(self):
#         print('Вход в цикл')
#         self.counter_1 = -1
#         return self

#     def __next__(self):
#         self.counter_1 += 1
#         if self.counter_1 == len(self.list_of_list):
#             print('Сработало прерывание цикла. Выход из цикла')
#             raise StopIteration
#         else:
#             item = self.list_of_list[self.counter_1]
#             return item


class IterObject:
    '''Итерируемый объект'''
    
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        
    def __iter__(self):
        '''Возвращаем итератор, чтобы соответствовать протоколу
        итератора'''
        return ClassIterator(self.list_of_list)

class ClassIterator:

    def __init__(self, list_of_list):
        self.current = 0
        self.list_of_list = list_of_list

    def __next__(self):
        if self.current >= len(self.list_of_list):
            print('Итератор исчерпан. Сработало прерывание цикла. Выход из цикла')
            raise StopIteration
        else:
            item = self.list_of_list[self.current]
            self.current += 1
            return item

    def __iter__(self):
        '''Чтобы соответствовать протоколу, каждый итератор должен
        одновременно быть итерируемым объектом'''
        print('Итератор сам являетс итерируемым объектом')
        return self

for x in IterObject([[1, 2, 3], [5, 6]]):
    for xx in x:
        print(xx)

# 1
# 2
# 3
# 5
# 6
