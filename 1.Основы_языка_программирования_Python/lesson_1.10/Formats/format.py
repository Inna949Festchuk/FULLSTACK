# ЧТЕНИЕ из файл.csv
# Оброботка построчная
# import csv
# with open('C:/Users/prepod/Desktop/ПИ/newsafr.csv', 'r') as f:
#     reader = csv.reader(f)
#     count = 0
#     for row in reader:
#         print(row[-1])
#         count += 1
# print(f'в файле {count - 1} статьи(-ей)')

# Обработка сразу всего файла
# import csv
# with open('C:/Users/prepod/Desktop/ПИ/newsafr.csv', 'r') as f:
#     reader = csv.reader(f)
#     # for row in reader:
#     #     print(row[-1])
#     #     count += 1
#     news_list = list(reader)
# header = news_list.pop(0) # Удаление заголовка .csv (перврй строки списка)
# for news in news_list:
#     print(news[-1])
# print(f'в файле {len(news_list)} статьи(-ей)')

# .csv в СЛОВАРЬ (заголовок файла через запятую - это ключи словаря)
import csv
with open('C:/Users/prepod/Desktop/ПИ/newsafr.csv', 'r') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        print(row['title'])
        count += 1
print(f'в файле {count} статьи(-ей)')

# ЗАПИСЬ в файл.csv
import csv

with open('C:/Users/prepod/Desktop/ПИ/newsafr.csv', 'r') as f:
    reader = csv.reader(f) 
    news_list = list(reader)
header = news_list.pop(0)

# with open('C:/Users/prepod/Desktop/ПИ/newsafr_write.csv', 'w') as f:
#     writer = csv.writer(f)
#     # Создаем заголовок
#     writer.writerow(header)
#     # Создаем статьи
#     # так
#     writer.writerows(news_list)
#     # или так (это одно и тоже)
#     # for row in news_list:
#     #     writer.writerow(row)

# Усли мы работаем с MS Excel, то делаем так
# with open('C:/Users/prepod/Desktop/ПИ/newsafr_write.csv', 'w') as f:
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

# Квотинг - управляем кавычками, чтобы прятать разделители.
# Например, запятую в дате "Oct, 21" 
with open('C:/Users/prepod/Desktop/ПИ/newsafr_write.csv', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL) # квотинг
    writer.writerow(header)
    writer.writerows(news_list)
   