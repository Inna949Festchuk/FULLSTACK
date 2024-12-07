## ПЕРВЫЙ СПОСОБ (второй ниже прошу обратить на него внимание и ответить на мой вопрос ниже во втором способе)
### Клонируйте проект с GitHub и перейдите в рабочую дирректорию проекта stocks_products:
```bash
git clone <URL репозитория>
cd stocks_products
```
### В рабочей дирректории проекта создайте фай .env и откройте в редакторе, например nano:
```bash
nano .env
```
### Пропишите в нем следующие переменные окружения и выйдите из редактора с сохранением (ЭТО ТОЛЬКО ДЛЯ ПРОВЕРКИ, НИКОГДА ТАК НЕ ДЕЛАЙ):
```bash
SECRET_KEY='django-insecure-nw^y+m^wmxza1asgk+)!ua2qx9)g+#v=6%76-9i8i(6eqiw94j'
DEBUG=True
ALLOWED_HOSTS=*
# Если используем sqlite3
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```
###  В рабочей дирректории проекта введите команду, применив миграции:
```bash
python manage.py migrate
```
### В рабочей директории проекта выполните команду для сборки образа:
```bash
docker build -t image_stocks_products:0.1 .
```
### В рабочей директории проекта запустите контейнер:
```bash
docker run -d --name=container_stocks_products -p 8080:8000 image_stocks_products:0.1
```
### Используйте файл `requests-examples.http` с расширением VSCode Rest Client для отправки запросов к эндпоинтам или введите в браузере: `http://localhost:8080/api/v1/`
## ВТОРОЙ СПОСОБ (мне кажется он безопаснее потому что файл `.env` не копируется в рабочую дирректорию контейнера (можно проверить `docker exec -it [CONTAINER_ID] sh`), а болтается где-то в другом месте контейнера, так ли это?)
### Перед сборкой образа поместите созданный ранее файл `.env` в файл исключений `.dockerignore`
### В рабочей директории проекта выполните команду для сборки образа верссии 0.2:
```bash
docker build -t image_stocks_products:0.2 .
```
### В рабочей директории проекта запустите контейнер container_stocks_products_2 изменив проброс портов и добавив ключ --env-file с указанием на созданный ранее файл .env:
```bash
docker run -d --name=container_stocks_products_2 -p 8081:8000 --env-file .env image_stocks_products:0.2
```
### Используйте файл `requests-examples.http` с расширением VSCode Rest Client для отправки запросов к эндпоинтам или введите в браузере: `http://localhost:8081/api/v1/`