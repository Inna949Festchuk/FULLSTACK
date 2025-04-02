# import uuid
# import os

# from flask import Flask
# from flask import request
# from flask.views import MethodView
# from flask import jsonify
# from celery import Celery
# from celery.result import AsyncResult

# from face_checker import FaceChecker



# app_name = 'app'
# app = Flask(app_name)
# app.config['UPLOAD_FOLDER'] = 'files'
# celery = Celery(
#     app_name,
#     backend='redis://localhost:6379/3',
#     broker='redis://localhost:6379/4'
# )
# celery.conf.update(app.config)

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery.Task = ContextTask


# @celery.task()
# def match_photos(path_1, path_2):

#     result = FaceChecker.with_files().match(path_1, path_2)
#     return result


# class Comparison(MethodView):

#     def get(self, task_id):
#         task = AsyncResult(task_id, app=celery)
#         return jsonify({'status': task.status,
#                         'result': task.result})
#     def post(self):
#         image_pathes = [self.save_image(field) for field in ('image_1', 'image_2')]
#         task = match_photos.delay(*image_pathes)
#         return jsonify(
#             {'task_id': task.id}
#         )

#     def save_image(self, field):
#         image = request.files.get(field)
#         extension = image.filename.split('.')[-1]
#         path = os.path.join('files', f'{uuid.uuid4()}.{extension}')
#         image.save(path)
#         return path


# comparison_view = Comparison.as_view('comparison')
# app.add_url_rule('/comparison/<string:task_id>', view_func=comparison_view, methods=['GET'])
# app.add_url_rule('/comparison/', view_func=comparison_view, methods=['POST'])


# if __name__ == '__main__':
#     app.run()

import uuid  # Импортируем модуль для генерации уникальных идентификаторов
import os  # Импортируем модуль для работы с файловой системой

from flask import Flask  # Импортируем основной класс Flask для создания приложения
from flask import request  # Импортируем объект request для обработки HTTP-запросов
from flask.views import MethodView  # Импортируем класс MethodView для создания контроллеров
from flask import jsonify  # Импортируем функцию jsonify для возврата JSON-ответов
from celery import Celery  # Импортируем класс Celery для асинхронных задач
from celery.result import AsyncResult  # Импортируем AsyncResult для получения состояния асинхронной задачи
from face_checker import FaceChecker  # Импортируем FaceChecker для сравнения изображений


app_name = 'app'  # Название приложения

app = Flask(app_name)  # Создаем экземпляр Flask

app.config['UPLOAD_FOLDER'] = 'files'  # Указываем папку для загрузки файлов

# Создаем экземпляр Celery с конфигурацией для брокера и бэкенда
celery = Celery(
    app_name,
    backend='redis://localhost:6379/3',  # Указываем бэкенд для хранения результатов
    broker='redis://localhost:6379/4'  # Указываем брокер для обработки задач
)

celery.conf.update(app.config)  # Обновляем конфигурацию Celery с настройками приложения


class ContextTask(celery.Task):
    """Класс для выполнения задач Celery с контекстом приложения Flask."""

    def __call__(self, *args, **kwargs):
        """Выполняет задачу с контекстом приложения Flask.

        Args:
            *args: Позиционные аргументы, переданные задаче.
            **kwargs: Именованные аргументы, переданные задаче.

        Returns:
            Результат выполнения задачи.
        """
        with app.app_context():  # Создаем контекст приложения
            return self.run(*args, **kwargs)  # Вызываем основную задачу


celery.Task = ContextTask  # Переопределяем класс задач Celery для использования контекста приложения


@celery.task()  # Декоратор для определения задачи Celery
def match_photos(path_1, path_2):
    """Сравнивает два изображения по заданным путям.

    Args:
        path_1 (str): Путь к первому изображению.
        path_2 (str): Путь ко второму изображению.

    Returns:
        Результат сравнения изображений.
    """
    result = FaceChecker.with_files().match(path_1, path_2)  # Вызываем метод FaceChecker для сравнения изображений
    return result  # Возвращаем результат сравнения


class Comparison(MethodView):
    """Класс для обработки запросов на сравнение изображений."""
    
    def get(self, task_id):
        """Обрабатывает GET-запрос для получения статуса задачи.

        Args:
            task_id (str): Идентификатор задачи.

        Returns:
            JSON-ответ с текущим статусом и результатом задачи.
        """
        task = AsyncResult(task_id, app=celery)  # Получаем информацию о задаче по ID
        return jsonify({'status': task.status, 'result': task.result})  # Возвращаем статус и результат задачи

    def post(self):
        """Обрабатывает POST-запрос для отправки изображений и запуска задачи.

        Returns:
            JSON-ответ с идентификатором задачи.
        """
        image_pathes = [self.save_image(field) for field in ('image_1', 'image_2')]  # Сохраняем загруженные изображения
        task = match_photos.delay(*image_pathes)  # Запускаем асинхронную задачу
        return jsonify({'task_id': task.id})  # Возвращаем ID задачи


    def save_image(self, field):
        """Сохраняет загруженное изображение и возвращает путь к нему.

        Args:
            field (str): Имя поля с изображением в запросе.

        Returns:
            str: Путь к сохраненному изображению.
        """
        image = request.files.get(field)  # Получаем изображение из запроса
        extension = image.filename.split('.')[-1]  # Получаем расширение файла
        path = os.path.join('files', f'{uuid.uuid4()}.{extension}')  # Генерируем уникальный путь для сохранения
        image.save(path)  # Сохраняем изображение
        return path  # Возвращаем путь к сохраненному изображению


comparison_view = Comparison.as_view('comparison')  # Создаем представление для обработки запросов
app.add_url_rule('/comparison/<string:task_id>', view_func=comparison_view, methods=['GET'])  # Регистрируем маршрут для получения статуса задачи
app.add_url_rule('/comparison/', view_func=comparison_view, methods=['POST'])  # Регистрируем маршрут для отправки изображений


if __name__ == '__main__':  # Проверяем, запущен ли скрипт напрямую
    app.run()  # Запускаем сервер Flask

