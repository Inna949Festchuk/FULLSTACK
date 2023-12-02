import time
import json
from tqdm import tqdm

from Class_VkFoto import VkFoto
from Class_YaUploader import YaUploader

if __name__ == '__main__':
    path_folder = input('Введите путь к Yandex папке: ')     
    path_to_file = 'metadates.json'
    token = input('Введите TOKEN: ')
    users_id = input('Введите идентификатор страницы пользователя: ')
    in_count = int(input('Введите количество выгружаемых фотографий: '))
    
    uploader = YaUploader(token)
    uploader.created_folder(path_folder)

    with open('tokenVK.txt', 'r') as file_object:
        token_vk = file_object.read().strip()
    vk_foto = VkFoto(token_vk)
    vk_foto_1 = vk_foto.profile_fotos(users_id, in_count)['response']
    counts = vk_foto.count

    try:
        for i in tqdm(range(int(counts))):
            # Получаем контент с сылкой на фото
            dicts_foto_1 = vk_foto_1['items'][i]['sizes']
            # Получаем дату добавления фото в профиль
            date_foto_1 = vk_foto_1['items'][i]['date']
            date_foto_1_utc = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime(date_foto_1))
            # Получаем количество лайкосов фотки профиля
            likes_foto_1 = vk_foto_1['items'][i]['likes']['count']
            # Делает новый словарь с ключом - размер фото 
            dct = {v['height'] * v['width']: v['url'] for v in dicts_foto_1}
            # Находим фото с максимальным размером
            max_dct = max(dct.items())
            # Создаем лист дубликатов лайков
            sheet_of_duplicates = []
            for j in range(int(counts)):
                if likes_foto_1 == vk_foto_1['items'][j]['likes']['count']:
                    sheet_of_duplicates.append(f'{likes_foto_1}_{date_foto_1_utc}')
                else:
                    sheet_of_duplicates.append(likes_foto_1)
            
            # Создаем json с информацией о фото
            with open ('metadates.json', 'a') as outfile:
                if counts == 1: # Если выгружается только одна фотка
                    js = [{"file_name": f"{likes_foto_1}.jpg", "size": f"{max_dct[0]} pixels"}]
                    # Загружаю foto по url на Ядиск
                    uploader.from_url_upload(max_dct[1], path_folder, likes_foto_1)
                else:
                    js = [{"file_name": f"{sheet_of_duplicates[i-1]}.jpg", "size": f"{max_dct[0]} pixels"}]
                    # Загружаю foto по url на Ядиск
                    uploader.from_url_upload(max_dct[1], path_folder, sheet_of_duplicates[i-1])
                json.dump(js, outfile, indent=2)

            # Загружаю локальный json файл на Ядиск
            uploader.files_upload(path_to_file, path_folder)

    except IndexError:
        print('Вы ввели большее количество фотографий чем есть у этого пользователя')
