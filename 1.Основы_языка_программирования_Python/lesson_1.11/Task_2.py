import requests
import os

# TOKEN = "..."

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
        }

    def upload(self, file_path: str):
        """Метод загружает файл file в папку на яндекс диск"""
        # Create folder on Yadisk
        upload_url_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        response_folder = requests.put(f'{upload_url_folder}?path={path_folder}', headers=headers)
        # Upload file to folder on Yadisk
        # Зарезервировать ссылку для загрузки файла
        upload_url_file = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        disk_file_path = f'{path_folder}/{os.path.basename(path_to_file)}'
        params = {"path": disk_file_path, "overwrite": "true"}  
        response = requests.get(upload_url_file, headers=headers, params=params) 
        result = response.json()
        # Загрузить файл по полученной ссылке
        href = result.get("href", "")
        response = requests.put(href, data=open(path_to_file, 'rb')) 
        if response.status_code == 201:
            print(f'Успех, файл {os.path.basename(path_to_file)} загружен '
                  f'в папку {path_folder}.'
            )

if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input('Введите путь к загружаемому файлу: ')
    path_folder = input('Введите путь к Yandex папке: ')
    token = input('Введите TOKEN: ')
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)

