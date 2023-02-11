import sys


import xml.etree.ElementTree as ET
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse("files/newsafr.xml", parser)
root = tree.getroot()
print(root.tag)
print(root.text)
print(root.attrib)

# news_list = root.find("channel/item")
# print(type(news_list))
# news_list = root.findall("channel/item")
# # print(type(news_list))
# for news in news_list:
# 	print(news.find("title").text)
# print(len(news_list))

titles_list = root.findall("channel/item/title")
for title in titles_list:
	print(title.text)



sys.exit()

import json

with open("files/newsafr.json") as f:
	json_data = json.load(f)

print(type(json_data))
news_list = json_data["rss"]["channel"]["items"]
# print(news_list[0])
for news in news_list:
	print(news["title"])
print(len(news_list))

with open("files/newsafr2.json", "w") as f:
	json.dump(json_data, f, ensure_ascii=False, indent=2)

sys.exit()

import csv

with open("files/newsafr.csv") as f:
	reader = csv.reader(f)
	# reader = csv.DictReader(f)
	# count = 0
	# for row in reader:
	# 	row["title"]
	# 	print(type(row))
	# 	print(row)
	# 	count += 1
	# for row in reader:
	# 	print(row[-1])
	# 	count += 1
		# print(row)
		# print(type(row))
	news_list = list(reader)
# print(f"В этом файле {count} статей")

header = news_list.pop(0)
# for news in news_list:
# 	print(news[-1])
# print(f"В этом файле {len(news_list)} статей")

print(news_list[:3])

csv.register_dialect("csv_commas_no_quote", delimiter=",", quoting=csv.QUOTE_NONE, escapechar="\\")

csv.register_dialect("csv_c_no_quote", delimiter=";")



# with open("files/newsafr2.csv", "w") as f:
# 	writer = csv.writer(f, "csv_c_no_quote")
# 	writer.writerow(header)
# 	# for row in news_list:
# 	# 	writer.writerow(row)
# 	writer.writerows(news_list)
# 	# writer.writerow("Hello")

# with open("files/newsafr2.csv", "w") as f:
# 	writer = csv.writer(f, "csv_c_no_quote")
# 	writer.writerow(header)

with open("files/newsafr2.csv", "a") as f:
	writer = csv.writer(f, "csv_c_no_quote")
	writer.writerows(news_list[:4])

















