from pprint import pprint
import requests

TOKEN = "..."



class YandexDisk:

    def __init__(self, token):
        self.token = token
    # Функция которая автоматически возвращает токен
    def get_headers(self):
        return {
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
        }
    # ФУНКЦИЯ ПОЛУЧЕНИЯ ДАННЫХ С ЯНДЕКС ДИСКА
    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        # где 
        # https://cloud-api.yandex.net/ - адрес API яндексдиска
        # v1/disk/resources/files - это конструкция get запроса для получения 
        # списка файлов упорядоченных по имени (см. https://yandex.ru/dev/disk/rest/)
        headers = self.get_headers()
        # Мы делаем get запрос по files_url 
        response = requests.get(files_url, headers=headers)
        # И нам возвращается результат
        return response.json()
    # ФУНКЦИЯ ПОЛУЧЕНИЯ ССЫЛКИ ДЛЯ ЗАГРУЗКИ ДАННЫХ НА ЯНДЕКС ДИСК
    def _get_upload_link(self, disk_file_path):
        # 2) Функция входит на яндекс диск по этому url
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        # 3) Запрашивает зарезервированную яндексом ссылку места  
        # куда мы хотим сохранить наш файл disk_file_path,
        params = {"path": disk_file_path, "overwrite": "true"} # overwrite - если файл уже есть он перезапишется
        # выполняя get запрос 
        response = requests.get(upload_url, headers=headers, params=params) # headers - результат функции get_headers() - токен 
        pprint(response.json())
        # 4) В РЕЗУЛЬТАТЕ НАМ ВОЗВРАЩАЕТСЯ СЛОВАРЬ В КОТОРОМ ЕСТЬ ССЫЛКА ДЛЯ ЗАГРУЗКИ
        return response.json()
    # ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ НА ЯНДЕКС ДИСКА
    def upload_file_to_disk(self, disk_file_path, filename):
        # disk_file_path - где будет лежать загружаемый файл на яндекс диске
        # filename - путь к загружаемому файлу на локалном диске
        # Запрашиваем ссылку зарезервированного на яндекс диске места для загрузки файла
        # Для этого 1) Обращаемся к функции выше _get_upload_link()
        result = self._get_upload_link(disk_file_path=disk_file_path)
        # 5) в словаре есть ключ href - это и есть ссылка для загрузки
        href = result.get("href", "")
        # 6) яндекс тебует выполнить метод put и отправили туда файл по ссылке href
        response = requests.put(href, data=open(filename, 'rb')) #  rb - двоичное чтение
        
        # raise_for_status() не обязательная функция принудительно останавливающая выполнение программы
        # если возникает ошибки на стороне сервера 4хх или клиента 5хх 
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")



# Создаем класс для работы с ЯндексДиском и в нем функцию
if __name__ == '__main__':
    ya = YandexDisk(token=TOKEN)
    # Вызываем функцию получения данных с яндекс диска
    # pprint(ya.get_files_list())
    # Вызываем функцию загрузки данных на яндекс диск
    pprint(ya.upload_file_to_disk('Неттология/test1006.txt', 'requestsPy/test.txt'))

