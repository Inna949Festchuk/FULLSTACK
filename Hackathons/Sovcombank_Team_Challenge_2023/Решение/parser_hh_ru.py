import requests
import re

from pprint import pprint
from bs4 import BeautifulSoup
from fake_headers import Headers
from tqdm import tqdm

HOST = "https://spb.hh.ru"
PARAMS = {
    "area":["1", "2"], # Код региона по ISO 3166-1 alpha-2, для Москвы - 1, для Питера - 2
    "search_field":["name", "company_name", "description"], # Поиск в названии вакансии, названии компании, описании вакансии
    "enable_snippets":"true",
    "text":"Python"+"django"+"flask", # Поиск по ключевым словам
    "no_magic":"true",
    "ored_clusters":"true",
    "items_on_page":"20", # Количество объявлений на странице
    "page":"0" # Номер страницы с объявлениями
}        
HOSTVACANCIES = f"{HOST}/search/vacancy"
HEADERS = Headers(browser="firefox", os="win").generate() # Притворяемся браузером "firefox" и ОС "win"

# Настраиваем прогрессбар
progress = tqdm(desc='Обрабатано', unit='страниц(ы)', bar_format='{desc}: {n_fmt} {unit}', leave=False)

finall_list = []
i = 1
while True: # выполняем пока не закончатся страницы

    try:
        
        # Получаем текст тела ответа на запрос
        response = requests.get(HOSTVACANCIES, params=PARAMS, headers=HEADERS)
        text = response.text
        
        # Готовим суп
        soup = BeautifulSoup(text, features='html.parser')     
        
        # Получаем название и ссылку объявления
        vacancies = soup.find_all("div", class_="serp-item")
        for vacancie in vacancies:
            vacancie_tag_a = vacancie.find("a", class_="serp-item__title")
            href = vacancie_tag_a.attrs['href']
            
            # Получаем зарплату
            salary = vacancie.find("span", class_="bloko-header-section-3")
            if salary != None:
                salary_el = salary.text
            else:
                salary_el = "Зарплата не указана!"

            # Получаем работадателя
            employer = vacancie.find("a", class_="bloko-link bloko-link_kind-tertiary").text # Поиск по классу

            # Получаем город
            city = vacancie.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text # Поиск по атрибуту

            # print(vacancie_tag_a.text, salary_el, employer, city, '-->', href)

            finall_dict = {
                "Вакансия":vacancie_tag_a.text,
                "Зарплата":re.sub(r"(\u202f)", " ", salary_el),
                "Работодатель":re.sub(r"(\xa0)", " ", employer),
                "Город":re.sub(r"(\xa01\xa0)", " ", city),
                "Ссылка":href
            }
            
            finall_list.append(finall_dict)

        # Узнаем максимальное количество страниц page для заданного items_on_page 
        max_pages = soup.find_all("span", class_="bloko-button bloko-button_pressed")[-1].text
        page = int(max_pages) - (int(max_pages) - i)
        # Переключаем на следующую страницу объявлений
        PARAMS["page"] = page 
        progress.update()
        i += 1
        
    except IndexError:
        print(f"\nПросмотрены все страницы!")
        break
        
pprint(finall_list)