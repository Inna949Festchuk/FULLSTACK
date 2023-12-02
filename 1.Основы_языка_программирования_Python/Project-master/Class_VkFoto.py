import requests

class VkFoto:
    url = 'https://api.vk.com/method/photos.get'
    def __init__(self, token_vk, version='5.131'):
        self.params = {
            'access_token': token_vk,
            'v': version    
        }
        
    def profile_fotos(self, owner_id, count=5):
        '''
        Метод выгружает заданное количество фотографий со страницы пользователя
        owner_id — идентификационный номер владельца аккаунта ВКонтакте
        count  - количество выгружаемых фото максимального размера
        '''
        self.count = count
        self.owner_id = owner_id
        profile_fotos_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True,
            'count': count
        }
        response = requests.get(self.url, params={**self.params, **profile_fotos_params}, timeout = 3).json()
        return response
    