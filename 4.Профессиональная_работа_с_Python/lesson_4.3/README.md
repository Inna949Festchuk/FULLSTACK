# Lesson 4.3.  Веб-скрапинг

### *Инструменты на python*:
- **Developer Tools** в браузере. На элементе страницы нажать F12 | ПКМ Indpect/Просмотреть код | Ctrl+Shift+I
- **reqests**. Для извлечения сырой разметки\
`pip install requests`
-  **Beautiful Soup**. Для легкого извлечения данных из сырой разметки\
`pip install beautifulsoup4`
- **reuests-html**.  Для извлечения сырой разметки на сайтах с динамически формируемым контентом + удобное извлечение данных из полученной разметки\
`pip install requests-html` (python 3.6+)
- **Silenium** + нужен драйвер. Эмулятор веб-браузера или полноценный веб-браузер, в зависимлсти от драйвера\
`pip install silenium`

### *Советы бывалого*:
- Если сайт не слишком защищается от парсеров и не требует JS для работы:
requests для скачивания страницы, beautiful soup для разбора html документа и поиска элементов в нём.

- Если сайт требует JS для работы, можно пошариться в консоли разработчика в браузере и найти, какие запросы страница-фронт делает, чтобы подгрузить данные. Тогда ты можешь научиться делать точно такие-же запросы, и получать данные сразу в машинночитаемом виде (часто в JSON).

- Если сайт защищается от парсеров и JS логика слишком сложная, или он часто обновляется, можно попробовать selenium для эмуляции браузера. Дальше используешь инструменты selenium, чтобы найти интересующие тебя элементы на странице.

- Если сайт детектит selenium, нужно искать сборки селениума, которые труднее обнаружить. Тут я навскидку не подскажу.

### Парсинг сайта Яндекс.Музыка на Python на основе Top-100

<details>
  
```python
import requests
from bs4 import BeautifulSoup

# URL чарта "Топ 100"
url = 'https://music.yandex.ru/chart/top-100'

# Отправляем GET-запрос на страницу
response = requests.get(url)

# Создаем объект BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Находим ссылку на первый трек в чарте
track_link = soup.find('a', class_='d-track__title-link')

# Получаем URL трека
track_url = track_link.get('href')

# Выводим URL трека
print(track_url)
```
</details>
  
### Учебный материал:
- [Самоучитель по Python для начинающих. Часть 17: Основы скрапинга и парсинга](https://proglib.io/p/samouchitel-po-python-dlya-nachinayushchih-chast-17-osnovy-skrapinga-i-parsinga-2023-03-13)
- [Beautiful Soup на русском языке](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)

### Дополнительные материалы:
- [Юридические аспекты скрапинга](http://ipcmagazine.ru/legal-issues/big-data-and-intellectual-property-a-systematic-study-of-scraping-as-part-of-a-common-internet-law-methodology)

### [Домашняя работа](./HomeTask_4_3)
