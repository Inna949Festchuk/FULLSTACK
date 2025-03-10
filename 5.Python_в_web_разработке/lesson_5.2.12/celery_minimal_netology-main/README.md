
### 1. Запускаем redis 

```shell
docker-compose up 
```

в выводе должна присутсвовать строка 

```
celery_minimal_netology-redis-1  | ...................... * Ready to accept connections
```

### 2. Запускаем celery

в другой вкладке терминал запускаем celery 

```shell
celery -A tasks.celery_app worker
```

должен получится вывод без ошибок и ворнингов наподобие такого:

```
 -------------- celery@python-gear v5.2.7 (dawn-chorus)
--- ***** ----- 
-- ******* ---- Linux-5.4.0-135-generic-x86_64-with-glibc2.31 2022-12-22 13:53:48
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         __main__:0x7f63c72023e0
- ** ---------- .> transport:   redis://127.0.0.1:6379/1
- ** ---------- .> results:     redis://127.0.0.1:6379/2
- *** --- * --- .> concurrency: 12 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
```

### 3. Запускаем приложение
Запускаем [main.py](main.py) через ide или командой 
```shell
python main.py
```