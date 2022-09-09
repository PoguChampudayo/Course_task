from datetime import datetime
import requests
import json
from collections import Counter
import os
class VKPhotoSaver:
    
    def __init__(self, VK_id:str, VK_token:str, photo_quantity:int = 5) -> None:
        self.VK_id = VK_id
        self.VK_token = VK_token
        self.folder = 'Фото с VK'
        self.photo_quantity = photo_quantity
        self.url = ('https://api.vk.com/method/')
        self.params = {
            'access_token' : self.VK_token,
            'v': '5.131'
        }

   
    def get_VK_photo_info(self):
        ''' Input: class attrubutes (self.VK_id).
            Output: photos from VK profile info pulled from response -> items (extended = 1)
            '''
        self.VK_method = ('photos.get')
        get_VK_photo_info_params = {
            'owner_id': self.VK_id,
            'album_id': 'profile',
            'extended': '1',
            'count': self.photo_quantity
        }
        req = requests.get(self.url + self.VK_method, params={**self.params, **get_VK_photo_info_params})
        try:
            return req.json()['response']['items']
        except KeyError:
            print('Произошла ошибка при получении информации с VK.com')
            os._exit(0)

    def get_max_VK_photos(self) -> dict:
        ''' Input: get_VK_photo_info result.
            Output: dict ({id:[url, type, likes_count, date]})
        '''
        response_items = self.get_VK_photo_info()
        result = {}
        unique_names = []
        for photo in response_items:
            for max_size_photo in photo['sizes'][::-1]:
                result.setdefault(photo['id'],[max_size_photo['url'], max_size_photo['type'], photo['likes']['count'], photo['date']])
                break
            unique_names.append(photo['likes']['count'])
        counter = Counter(unique_names)
        for photo in result:
            if counter[result[photo][2]] > 1:
                photo_date = datetime.fromtimestamp(result[photo][3])
                result[photo][2] = str(result[photo][2]) + '_' + photo_date.strftime('%d-%m-%Y')
        return result

