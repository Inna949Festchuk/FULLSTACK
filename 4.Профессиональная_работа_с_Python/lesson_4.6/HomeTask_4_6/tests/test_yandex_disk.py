import os
import unittest
import requests

class TestYandexDiskFolderCreation(unittest.TestCase):
    '''
    Тест unittest test_yandex_disk.py проверяет, успешно ли создана папка 
    и существует ли она на Яндекс Диске. При желании он также удаляет папку после теста 

    !ВНИМАНИЕ! Если папка уже создана сторонним приложением запускаем только тест №_2

    1. Перед запуском теста убедитесь, что Oauth-токен Яндекс Диска сохранен как переменная среды 
    с именем YANDEX_DISK_TOKEN, для чего необходимо установить переменную среды, как показано ниже

    Установка переменную среды в Linux или macOS:
    export YANDEX_DISK_TOKEN="your_token_here"

    Установка переменную среды в Windows:
    set YANDEX_DISK_TOKEN=your_token_here

    2. Запустить тест с помощью следующей команды:
    
    python -m unittest tests/test_yandex_disk.py -v для MacOS
    py -m unittest tests/test_yandex_disk.py -v для Windows
    где -v - расширенная информация о результатах теста
    '''

    def setUp(self):
        self.token = os.environ['YANDEX_DISK_TOKEN']
        self.folder_name = input('Введите имя папки: ') # Если тестим стороннее приложение 
        # сюда из него импортируем переменную, содержащую имя папки (н-р: from app import folder_name)
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.request_headers = {
            'Authorization': f'OAuth {self.token}'
        }

    def tearDown(self):
        '''
        Повторяемые действия для всех тестов в конце тестирования
        '''
        pass

    def test_folder_creation(self):
        # Create the folder
        response = requests.put(
            f'{self.base_url}?path={self.folder_name}',
            headers=self.request_headers
        )
        # Проверяем, создалась ли папка (код 201-ОК иначе "Folder creation failed!")
        self.assertEqual(response.status_code, 201, "Folder creation failed!")

        # Check if the folder exists (!ВНИМАНИЕ! Если папка создана сторонним приложением запускаем только этот тест)
        response = requests.get(
            f'{self.base_url}?path={self.folder_name}',
            headers=self.request_headers
        )
        # Проверяем, появилась ли (существует ли) папка в списке файлов нв Я.Диске (код 200-ОК)
        self.assertEqual(response.status_code, 200, "Folder not found!")

        # # Clean up - delete the folder (optional)
        # response = requests.delete(
        #     f'{self.base_url}?path={self.folder_name}',
        #     headers=self.request_headers
        # )
        # # Проверяем, удалилась ли папка (код 204-ОК)
        # self.assertEqual(response.status_code, 204, "Delete folder failed!")

if __name__ == '__main__':
    unittest.main()

