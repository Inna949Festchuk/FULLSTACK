

Пример использования celery + rabbitmq в Docker

## Запуск

```bash
docker-compose up broker # запуск rabbitmq
docker-compose up db # запуск postgres
docker-compose up celery # запуск celery
docker-compose up app # запуск приложения
```