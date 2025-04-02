
# import os

# import dlib
# from skimage.io import imread
# from scipy.spatial import distance



# class FaceChecker:

#     instance = None

#     def __init__(self, shape_predictor, face_model):
#         self.shape_predictor = shape_predictor
#         self.face_model = face_model
#         self.face_detector = dlib.get_frontal_face_detector()

#     @classmethod
#     def with_files(cls,
#                    shape_predictor_path=os.path.join('models', 'shape_predictor_68_face_landmarks.dat'),
#                    face_model_path=os.path.join('models', 'dlib_face_recognition_resnet_model_v1.dat')):
#         if not cls.instance:
#             shape_predictor = dlib.shape_predictor(shape_predictor_path)
#             face_model = dlib.face_recognition_model_v1(face_model_path)
#             cls.instance = cls(shape_predictor, face_model)
#         return cls.instance

#     def load_image(self, path: str, visual=False):
#         img = imread(path)
#         rectangles = self.face_detector(img, 0)
#         shape = self.shape_predictor(img, rectangles[0])
#         if visual:
#             window = dlib.image_window()
#             window.clear_overlay()
#             window.set_image(img)

#             window.add_overlay(rectangles)
#             window.add_overlay(shape)
#             window.wait_until_closed()

#         descriptor = self.face_model.compute_face_descriptor(img, shape)
#         return descriptor

#     def match(self, img_path_1: str, img_path_2: str, visual=False):
#         return distance.euclidean(self.load_image(img_path_1, visual), self.load_image(img_path_2, visual), ) < 0.6


import os  # Импортируем модуль для работы с файловой системой
import dlib  # Импортируем библиотеку dlib для работы с детекцией лиц

from skimage.io import imread  # Импортируем функцию imread для чтения изображений
from scipy.spatial import distance  # Импортируем модуль distance для вычисления расстояния


class FaceChecker:
    """Класс для распознавания и сравнения лиц на изображениях."""

    instance = None  # Параметр для хранения единственного экземпляра класса

    def __init__(self, shape_predictor, face_model):
        """Инициализирует FaceChecker с моделью предсказания формы и моделью распознавания лиц.

        Args:
            shape_predictor: Модель для предсказания формы лиц.
            face_model: Модель для распознавания лиц.
        """
        self.shape_predictor = shape_predictor  # Модель предсказания формы
        self.face_model = face_model  # Модель распознавания лиц
        self.face_detector = dlib.get_frontal_face_detector()  # Инициализация детектора лиц

    @classmethod
    def with_files(cls,
                   shape_predictor_path=os.path.join('models', 'shape_predictor_68_face_landmarks.dat'),
                   face_model_path=os.path.join('models', 'dlib_face_recognition_resnet_model_v1.dat')):
        """Создает экземпляр FaceChecker с указанными моделями.

        Args:
            shape_predictor_path (str): Путь к файлу модели предсказания формы.
            face_model_path (str): Путь к файлу модели распознавания лиц.

        Returns:
            FaceChecker: Экземпляр класса FaceChecker.
        """
        if not cls.instance:  # Проверяем, существует ли уже экземпляр класса
            shape_predictor = dlib.shape_predictor(shape_predictor_path)  # Загружаем модель предсказания формы
            face_model = dlib.face_recognition_model_v1(face_model_path)  # Загружаем модель распознавания лиц
            cls.instance = cls(shape_predictor, face_model)  # Создаем новый экземпляр класса
        return cls.instance  # Возвращаем экземпляр класса

    def load_image(self, path: str, visual=False):
        """Загружает изображение и возвращает дескриптор лица.

        Args:
            path (str): Путь к изображению.
            visual (bool): Если True, отображает изображение с детектированными лицами.

        Returns:
            descriptor: Дескриптор лица.
        """
        img = imread(path)  # Читаем изображение
        rectangles = self.face_detector(img, 0)  # Находим лицо на изображении
        shape = self.shape_predictor(img, rectangles[0])  # Получаем координаты важнейших точек лица

        if visual:  # Если visual установлен в True
            window = dlib.image_window()  # Открываем окно для отображения
            window.clear_overlay()  # Очищаем предыдущие наложения
            window.set_image(img)  # Устанавливаем изображение

            window.add_overlay(rectangles)  # Добавляем наложение для найденных лиц
            window.add_overlay(shape)  # Добавляем наложение для ключевых точек лиц
            window.wait_until_closed()  # Ждем, пока окно не будет закрыто

        descriptor = self.face_model.compute_face_descriptor(img, shape)  # Вычисляем дескриптор лица
        return descriptor  # Возвращаем дескриптор

    def match(self, img_path_1: str, img_path_2: str, visual=False):
        """Сравнивает два изображения и определяет, являются ли лица на них одинаковыми.

        Args:
            img_path_1 (str): Путь к первому изображению.
            img_path_2 (str): Путь ко второму изображению.
            visual (bool): Если True, отображает изображение с детектированными лицами.

        Returns:
            bool: True, если лица совпадают, иначе False.
        """
        return distance.euclidean(self.load_image(img_path_1, visual), 
                                   self.load_image(img_path_2, visual)) < 0.6  # Возвращаем результат сравнения
