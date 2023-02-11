# - - - - - - - - - - - - - - - - -

# ЧТЕНИЕ из файл.csv
# Оброботка построчная
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f)
#     count = 0
#     for row in reader:
#         print(row[-1])
#         count += 1
# print(f'в файле {count - 1} статьи(-ей)')

# - - - - - - - - - - - - - - - - - 

# Обработка сразу всего файла
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f)
#     # for row in reader:
#     #     print(row[-1])
#     #     count += 1
#     news_list = list(reader)
# header = news_list.pop(0) # Удаление заголовка .csv (перврй строки списка)
# for news in news_list:
#     print(news[-1])
# print(f'в файле {len(news_list)} статьи(-ей)')

# - - - - - - - - - - - - - - - - - 

# .csv в СЛОВАРЬ (заголовок файла через запятую - это ключи словаря)
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     count = 0
#     for row in reader:
#         print(row['title'])
#         count += 1
# print(f'в файле {count} статьи(-ей)')

# - - - - - - - - - - - - - - - - - 

# # ЗАПИСЬ в файл.csv
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f) 
#     news_list = list(reader)
# header = news_list.pop(0)

# with open('files/newsafr_write.csv', 'w') as f:
#     writer = csv.writer(f)
#     # Создаем заголовок
#     writer.writerow(header)
#     # Создаем статьи
#     # так
#     writer.writerows(news_list)
#     # или так (это одно и тоже)
#     # for row in news_list:
#     #     writer.writerow(row)

# - - - - - - - - - - - - - - - - - 

# Если мы работаем с MS Excel, то делаем так
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f) 
#     news_list = list(reader)
# header = news_list.pop(0)
# with open('files/newsafr_write.csv', 'w') as f:
#     writer = csv.writer(f, delimiter=';') # Установка разделителя 
#                                           # вместо "," (по-умолчанию) устанавливаем ";"
#     # Создаем заголовок
#     writer.writerow(header)
#     # Создаем статьи
#     # так
#     writer.writerows(news_list)
#     # или так (это одно и тоже)
#     # for row in news_list:
#     #     writer.writerow(row)

# - - - - - - - - - - - - - - - - - 

# Квотинг - управляем кавычками, чтобы прятать разделители.
# Например, запятую в дате "Oct, 21"
# import csv
# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f) 
#     news_list = list(reader)
# header = news_list.pop(0) 
# with open('files/newsafr_write.csv', 'w') as f:
#     # writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL) # квотинг
#     # QUOTE_MINIMAL - отделяет кавычками только если в строке есть запятая которая
#     # не должна использоваться как разделитель (например в дате "Thu, 17 Dec 2015 19:13 +0300")
#     # writer = csv.writer(f, quoting=csv.QUOTE_ALL) # квотинг
#     # QUOTE_ALL - отделяет кавычками все элементы строк 
#     # writer = csv.writer(f, quoting=csv.QUOTE_NONE) # квотинг
#     # QUOTE_NONE - убирает кавычки везде 
#     writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar="\\") # квотинг
#     # QUOTE_NONE - убирает кавычки везде 
#     # escapechar="\\" ставит перед разделителем - запятой обратный слэш (\) делая из разделителя безобидный символ - запятую
#     writer.writerow(header)
#     writer.writerows(news_list)

# - - - - - - - - - - - - - - - - - 

# ДИАЛЕКТ - регистрация набора настроек register_dialect()
# import csv
# csv.register_dialect("csv_commas_no_quote", 
#                     delimiter=',', quoting=csv.QUOTE_NONE, escapechar="\\") # Запихиваем сюда все настройки (это ДИАЛЕКТ_1)

# csv.register_dialect("csv_point_commas_no_quote", 
#                     delimiter=';') # Другой вариант диалекта (ДИАЛЕКТ_2) и так далее

# with open('files/newsafr.csv', 'r') as f:
#     reader = csv.reader(f) 
#     news_list = list(reader)
# header = news_list.pop(0) 

# with open('files/newsafr_write.csv', 'w') as f:
#     # writer = csv.writer(f, "csv_commas_no_quote") # вставляем сюда настроенный ДИАЛЕКТ_1
#     writer = csv.writer(f, "csv_point_commas_no_quote") # вставляем сюда настроенный ДИАЛЕКТ_2
#     writer.writerow(header)
#     writer.writerows(news_list)

# - - - - - - - - - - - - - - - - - 

# ДОПИСЫВАНИЕ в файл.csv - 'a' - append
# Например, для создания ЛОГОВ (LOG-файлов обработки данных)
import csv
csv.register_dialect("csv_commas_no_quote", 
                    delimiter=',', quoting=csv.QUOTE_NONE, escapechar="\\")

with open('files/newsafr.csv', 'r') as f:
    reader = csv.reader(f) 
    news_list = list(reader)
header = news_list.pop(0) 

# Создаем заголовок
with open('files/newsafr_write.csv', 'w') as f: 
    writer = csv.writer(f, "csv_commas_no_quote")
    writer.writerow(header)
# Дописываем, например, 4 новые статьи - 'a' - append
with open('files/newsafr_write.csv', 'a') as f: 
    writer = csv.writer(f, "csv_commas_no_quote")
    writer.writerows(news_list[:4])