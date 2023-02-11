# Мультиплатформенность (недоработан)
# import os
# current = os.getcwd()
# # folder_name = 'Task_3'
# file_name = '1.txt'
# file_path = os.path.join(current, file_name)
# # file = open(file_path)
# file = os.path.basename(file_path)
# print(file)

# ФИНАЛЬНЫЙ ВАРИАНТ (ДЛЯ ПРОВЕРКИ)
# Создание функции парссинга файлов file_pars(file_name)
def file_pars(file_name):
    file_path = open(file_name, 'rt', encoding = 'utf8')
    content = file_path.readlines() # Разделение контента файла по-строкам
    lenght_list = len(content) # Вычисление числа строк в файле
    # Формирование списка из номеров строк
    str_number = []
    for element in content:
        str_number.append(content.index(element) + 1)
    file_path.close()
    return file_name, lenght_list, str_number
# Выполнения функции парссинга входных файлов (ЭТО ИНТЕРФЕЙС)
file_pars_list = [
    file_pars('1.txt'),
    file_pars('2.txt'),
    file_pars('3.txt'),
    ]
# Формирование словаря, где ключ - это lenght_list, 
# а значения ключа список [file_name, str_number]
myDictionary = {}
for n in file_pars_list:
    myDictionary[n[1]] = [n[0], n[2]]
# Сортировка словаря по значению ключа (числа строк)       
sorted_keys = sorted(myDictionary.keys())
for k in sorted_keys:
    print(myDictionary[k][0], k, sep = '\n')
    for ss in myDictionary[k][1]:
        print(f'Строка номер {ss} файла номер {myDictionary[k][0][:-4]}')

# Предыдущий вариант (без автоматизации создания словаря)
# # Создание функции парссинга файлов file_pars(file_name)
# def file_pars(file_name):
#     file_path = open(file_name, 'rt', encoding = 'utf8')
#     content = file_path.readlines() # Разделение контента файла по-строкам
#     lenght_list = len(content) # Вычисление числа строк в файле
#     # Формирование списка из номеров строк
#     str_number = []
#     for element in content:
#         str_number.append(content.index(element) + 1)
#     file_path.close()
#     return file_name, lenght_list, str_number

# # Выполнения функции парссинга
# file_pars_1 = file_pars('1.txt')
# file_pars_2 = file_pars('2.txt')
# file_pars_3 = file_pars('3.txt')
# # Формирование и сортировка словаря по значению ключа (числа строк)
# myDictionary = {
#     file_pars_1[1]:[file_pars_1[0], file_pars_1[2]], 
#     file_pars_2[1]:[file_pars_2[0], file_pars_2[2]], 
#     file_pars_3[1]:[file_pars_3[0], file_pars_3[2]]
#     }
# sorted_keys = sorted(myDictionary.keys())
# for k in sorted_keys:
#     print(myDictionary[k][0], k, sep = '\n')
#     for ss in myDictionary[k][1]:
#         print(f'Строка номер {ss} файла номер {myDictionary[k][0][:-4]}')

# Предыдущий вариант (без функции парссинга)
# with open('1.txt', 'rt', encoding = 'utf8') as file_1:
#     print(file_1)
#     content_1 = file_1.readlines()
#     lenght_list_1 = len(content_1) # Вычисление числа строк в файле
#     # Формирование списка из номеров строк
#     str_number_1 = []
#     for element_1 in content_1:
#         str_number_1.append(content_1.index(element_1) + 1)
        
# with open('2.txt', 'rt', encoding = 'utf8') as file_2:
#     content_2 = file_2.readlines()
#     lenght_list_2 = len(content_2)

#     str_number_2 = []    
#     for element_2 in content_2:
#         str_number_2.append(content_2.index(element_2) + 1)

# with open('3.txt', 'rt', encoding = 'utf8') as file_3:
#     content_3 = file_3.readlines()
#     lenght_list_3 = len(content_3)
    
#     str_number_3 = []
#     for element_3 in content_3:
#         str_number_3.append(content_3.index(element_3) + 1)

# # Формирование и сортировка словаря по значению ключа (числа строк)
# myDictionary = {lenght_list_1:[file_1.name, str_number_1], lenght_list_2:[file_2.name, str_number_2], lenght_list_3:[file_3.name, str_number_3]}
# sorted_keys = sorted(myDictionary.keys())
# for k in sorted_keys:
#     print(myDictionary[k][0], k, sep = '\n')
#     for ss in myDictionary[k][1]:
#         print(f'Строка номер {ss} файла номер {myDictionary[k][0][:-4]}')

