# Подключение библиотеки
import xml.etree.ElementTree as ET # ET это АЛИАС - короткое имя
# Чтение xml
# tree = ET.parsel('files/newsafr.xml') # Указываем кодировку, она прописывается в заголовке исходного xml-файла
# Например <?xml version='1.0' encoding='windows-1251'?> и збивает с толку Питон, т.к. он работает с utf8
# поэтому необходимо принудительно Питону указывать encoding='utf-8'
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse("files/newsafr.xml", parser) 
root = tree.getroot()
print(root.tag) # Узнаем как его зовут
print(root.text) # Узнаем его текст, если он есть между открывающим и закрывающим тегами
print(root.attrib) # Узнаем его атрибут
# Перебираем иерархическую 
# структуру от корня и далее и добираемся до нужных нам данных !ЭТО ВАЖНО!
news_list = root.findall("channel/item")
for news in news_list:
    print(news.find("title")) # выводит адреса <Element 'title' at 0x101586e80>
# так как xml работает с адресами -> необходимо использовать функцию .text
    print(news.find("title").text)
print(len(news_list))

# Можно сделать проще
titles_list = root.findall("channel/item/title")
for title in titles_list:
	print(title.text)

# ЗАПИСЬ красивенько с отступами СМОТРИ В ПРЕЗЕНТАЦИИ СЛАЙД
tree.write('files/newsafr_write.xml', encoding="utf-8")