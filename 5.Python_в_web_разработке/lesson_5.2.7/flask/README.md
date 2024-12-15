## Дополнительные материалы
### [Документация Flask](https://flask.palletsprojects.com/en/stable/)
### [RESTful Authentication with Flask](https://blog.miguelgrinberg.com/post/restful-authentication-with-flask)

## Настройка дебагера
1. Создать и активировать виртуальную среду
2. Выбрать исполняемый интерпритатор python
3. [Отладка приложений на FLASK](https://code.visualstudio.com/docs/python/tutorial-flask)

- - - - - - - - - - - - - - - - - - - - 
### environment на Mac:
```bash
conda activate //anaconda3/envs/condageoenv
```
- - - - - - - - - - - - - - - - - - - - 



## Если не использовать condageoenv
## РЕШЕНИЕ ПРОБЛЕММ:

### Установка psycopg2

Для установки драйвера смени путь `PATH=$PATH:/Applications/Postgres.app/Contents/Versions/12/bin/ pip install psycopg2`

### Добавьте путь к утилитам Postgresql:
```bash
export PATH="/Applications/Postgres.app/Contents/Versions/12/bin/:$PATH"
```

### Если будет ошибка 
Ошибка, модуль `psycopg2` не может связаться с библиотекой `PostgreSQL` (`libpq`), так как она не содержит символа `_PQencryptPasswordConn`. Эта ситуация может возникнуть из-за несоответствия между установленной версией библиотек PostgreSQL и версией, ожидаемой модулем `psycopg2`.

### РЕШЕНИЕ:
Обновите путь к библиотекам: Убедитесь, что ваша среда указывает на правильную версию библиотек `PostgreSQL`. Это можно сделать, добавив путь к библиотекам `PostgreSQL` в переменную окружения `DYLD_LIBRARY_PATH:`

```bash
export DYLD_LIBRARY_PATH="/Applications/Postgres.app/Contents/Versions/12/lib:$DYLD_LIBRARY_PATH"
```
