from dataclasses import fields
import requests
from pprint import pprint


class VKPhotoSaver:
    
    def __init__(self, VK_id, ya_token = None) -> None:
        self.ya_token = ya_token
        self.VK_id = VK_id
        with open('VKtoken.txt', encoding='utf-8') as f:
            self.VK_token= f.read().split()
        self.url = ('https://api.vk.com/method/')
        self.params = {
            'access_token' : self.VK_token,
            'v': '5.131'
        }
    
   
    def get_VK_photo_info(self):
        self.VK_method = ('photos.get')
        get_VK_photo_info_params = {
            'owner_id': self.VK_id,
            'album_id': 'profile',
        }
        req = requests.get(self.url + self.VK_method, params={**self.params, **get_VK_photo_info_params})
        return req.json()['response']['items']

my_app = VKPhotoSaver('1')
photos = my_app.get_VK_photo_info()
# pprint(photos[0]['sizes'])
result = []
for photo in photos:
    for max_size_photo in photo['sizes']:
        if max_size_photo['type'] == 'z':
            result.append(max_size_photo)
pprint(result)