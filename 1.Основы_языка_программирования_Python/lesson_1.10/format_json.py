import json
# Открытие JSON
# with open("files/newsafr.json") as f:
#     json_data = json.load(f)
# news_list = json_data['rss']['channel']['items'] # Перебираем иерархическую 
# структуру от корня и далее и добираемся до нужных нам данных !ЭТО ВАЖНО! 
# print(news_list[0])
# for news in news_list:
#     print(news['title'])
# print(len(news_list))

# Запись JSON
with open("files/newsafr.json", 'r') as f:
    json_data = json.load(f)
with open("files/newsafr_write.json", 'w') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2) 
    # второй параметр f - это название записывамого файла
    # третий параметр ensure_ascii=False вводим, если нарушается кодировка Кирилицы
    # четвертый параметр indent=2 (2 это число отступов при каждом ветвлении) 
    # если мы хотим красивенько с отступами, т.к. Питон записывает все в одну строку