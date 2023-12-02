import requests
import os
from urllib.parse import quote

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
        }

    def created_folder(self, path_folder: str):
        ''' Метод создает папку на яндекс диске 
        path_folder - (строка) имя папки на яндекс диске
        '''
        # Create folder on Yadisk
        api_create_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        response_folder = requests.put(f'{api_create_folder}?path={path_folder}', headers=headers)
        # if response_folder.status_code == 201:
        #     print(f'Success, folder {path_folder} created.')

    def files_upload(self, path_to_file: str, path_folder):
        ''' Метод загружает локальный файл в папку на яндекс диск 
        path_to_file - (строка) путь к локальному файлу
        path_folder - (строка) имя папки на яндекс диске
        '''
        # Upload file to folder on Yadisk
        # Зарезервировать ссылку для загрузки файла
        api_file_download_link = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        disk_file_path = f'{path_folder}/{os.path.basename(path_to_file)}'
        params = {"path": disk_file_path, "overwrite": "true"}  
        response_folder = requests.get(api_file_download_link, headers=headers, params=params)
        # if response_folder.status_code == 200:
        #     print(f'Success, file download link received.')
        result = response_folder.json()
        # Загрузить файл по полученной ссылке
        href = result.get("href", "")
        response_download = requests.put(href, data=open(path_to_file, 'rb')) 
        # if response_download.status_code == 201:
        #     print(f'Success, файл {os.path.basename(path_to_file)} загружен '
        #           f'в папку {path_folder}.')

    def from_url_upload(self, url_to_files: str, path_folder, file_name='new'):
        ''' Метод загружает файл по url в папку на яндекс диск 
        url_to_files - (строка) ссылка на фото
        path_folder - (строка) имя папки на яндекс диске
        file_name - (строка) имя файла на яндекс диске
        '''
        headers = self.get_headers()
        api_upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        path_upload = f'{path_folder}/{file_name}'
        # url-кодирование 
        url_encoding = quote(url_to_files, safe='') 
        response_download_url = requests.post(f'{api_upload_url}?path={path_upload}&url={url_encoding}', headers=headers) 
        # if response_download_url.status_code == 202:
        #     print(f'Success, files by url loaded.')
